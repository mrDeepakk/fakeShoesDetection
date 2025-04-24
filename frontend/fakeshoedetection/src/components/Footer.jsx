import toast from "react-hot-toast";

export default function Footer() {
  const handleSubscribe = async (e) => {
    e.preventDefault();
    const email = e.target.email.value;

    const toastId = toast.loading("Subscribing...");

    try {
      const res = await fetch("http://localhost:8000/subscribe", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email }),
      });

      const data = await res.json();

      if (res.ok) {
        toast.success(data.message, { id: toastId });
        e.target.reset(); // Clear the form
      } else {
        toast.error(data.message || "Subscription failed", { id: toastId });
      }
    } catch (err) {
      toast.error("Network error. Please try again.", { id: toastId });
    }
  };

  return (
    <footer className="bg-gray-900 text-gray-400 border-t border-gray-800 py-10">
      <div className="max-w-7xl mx-auto grid sm:grid-cols-4 grid-cols-2 gap-6 px-6">
        <div>
          <h2 className="text-white text-lg font-semibold mb-3">Tools</h2>
          <ul className="space-y-2 text-sm">
            <li>
              <a className="hover:text-white transition">Image Upload</a>
            </li>
            <li>
              <a className="hover:text-white transition">Camera Scan</a>
            </li>
            <li>
              <a className="hover:text-white transition">Result Analysis</a>
            </li>
          </ul>
        </div>
        <div>
          <h2 className="text-white text-lg font-semibold mb-3">Company</h2>
          <ul className="space-y-2 text-sm">
            <li>
              <a className="hover:text-white transition">About</a>
            </li>
            <li>
              <a className="hover:text-white transition">Team</a>
            </li>
            <li>
              <a className="hover:text-white transition">Contact</a>
            </li>
          </ul>
        </div>
        <div>
          <h2 className="text-white text-lg font-semibold mb-3">Legal</h2>
          <ul className="space-y-2 text-sm">
            <li>
              <a className="hover:text-white transition">Terms</a>
            </li>
            <li>
              <a className="hover:text-white transition">Privacy</a>
            </li>
            <li>
              <a className="hover:text-white transition">Cookies</a>
            </li>
          </ul>
        </div>
        <div>
          <h2 className="text-white text-lg font-semibold mb-3">Newsletter</h2>
          <form className="flex flex-col space-y-2" onSubmit={handleSubscribe}>
            <input
              type="email"
              name="email"
              required
              placeholder="you@example.com"
              className="bg-gray-800 border border-gray-700 px-4 py-2 rounded-md text-white placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
            <button className="bg-emerald-500 hover:bg-emerald-600 text-white py-2 rounded-md font-medium transition">
              Subscribe
            </button>
          </form>
        </div>
      </div>
      <p className="text-center text-xs text-gray-600 mt-8">
        &copy; {new Date().getFullYear()} FakeShoeDetector. All rights reserved.
      </p>
    </footer>
  );
}
