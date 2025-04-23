// components/ResultModal.jsx
import React from "react";

export default function ResultModal({ result, onClose }) {
  return (
    <div className="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-gray-800 border border-gray-700 text-white rounded-2xl p-6 w-full max-w-sm shadow-2xl animate-fade-in">
        <h3 className="text-xl font-bold text-emerald-400 mb-2">
          Prediction Result
        </h3>
        <p className="text-lg">
          <span className="font-medium text-gray-300">Label:</span> {result}
        </p>
        <button
          onClick={onClose}
          className="mt-4 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-xl transition-all"
        >
          Close
        </button>
      </div>
    </div>
  );
}
