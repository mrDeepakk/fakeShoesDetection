import { useState, useRef } from "react";
import ResultModal from "./ResultModel";
import { toast } from "react-hot-toast";

export default function ImageUploader() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef();

  const handleImageChange = (file) => {
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setImage(imageUrl);
      setResult(null); // reset result
    }
  };

  const handleFileInput = (e) => {
    const file = e.target.files[0];
    handleImageChange(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    handleImageChange(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleVerify = async () => {
    setLoading(true);
    setResult(null);

    const file = fileInputRef.current.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/predict/", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (data.result?.label) {
        setResult(data.result.label);
        toast.success("Prediction successful!");
      } else {
        toast.error("Prediction failed!");
      }
    } catch (error) {
      toast.error("Something went wrong!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-gray-100 px-4">
      <div className="bg-gray-800 p-6 rounded-2xl shadow-xl w-full max-w-md text-center border border-gray-700">
        <h2 className="text-2xl font-bold mb-4">Upload Shoe Image</h2>

        {/* 📦 Drag & Drop */}
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          className="border-2 border-dashed border-gray-600 rounded-xl p-6 mb-4 cursor-pointer hover:border-emerald-400 transition"
          onClick={() => fileInputRef.current.click()}
        >
          <p className="text-sm text-gray-400">
            Drag & drop an image here, or{" "}
            <span className="text-emerald-400 font-medium">
              click to browse
            </span>
          </p>
        </div>

        {/* 📷 Camera & File Input */}
        <div className="flex justify-center gap-4 mt-2 mb-4">
          <label className="bg-emerald-500 hover:bg-emerald-600 text-white font-medium px-4 py-2 rounded-xl transition-all cursor-pointer">
            Camera
            <input
              type="file"
              accept="image/*"
              capture="environment"
              className="hidden"
              onChange={handleFileInput}
            />
          </label>

          <label className="bg-emerald-500 hover:bg-emerald-600 text-white font-medium px-4 py-2 rounded-xl transition-all cursor-pointer">
            Gallery
            <input
              type="file"
              accept="image/*"
              className="hidden"
              onChange={handleFileInput}
              ref={fileInputRef}
            />
          </label>
        </div>

        {/* 🔍 Image Preview */}
        {image && (
          <div className="mt-6">
            <h3 className="mb-2 font-medium">Preview:</h3>
            <img
              src={image}
              alt="Selected"
              className="w-full h-auto rounded-xl border-2 border-gray-700 mb-4"
            />

            <button
              onClick={handleVerify}
              className="bg-indigo-500 hover:bg-indigo-600 text-white font-medium px-6 py-2 rounded-xl transition-all disabled:opacity-50"
              disabled={loading}
            >
              {loading ? "Verifying..." : "Verify"}
            </button>
          </div>
        )}
      </div>

      {/* 🔔 Result Modal */}
      {result && (
        <ResultModal result={result} onClose={() => setResult(null)} />
      )}
    </div>
  );
}
