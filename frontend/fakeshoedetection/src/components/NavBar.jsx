import { useState } from "react";
import { Menu, X } from "lucide-react";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-gray-900/80 backdrop-blur-md border-b border-gray-800 text-white px-6 py-4 shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <h1 className="text-2xl font-bold bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
          FakeShoeDetector
        </h1>

        {/* Desktop Menu */}
        <ul className="hidden md:flex space-x-6 text-sm font-medium">
          <li>
            <a
              href="#"
              className="hover:text-emerald-400 transition duration-200"
            >
              Home
            </a>
          </li>
          <li>
            <a
              href="#"
              className="hover:text-emerald-400 transition duration-200"
            >
              About
            </a>
          </li>
          <li>
            <a
              href="#"
              className="hover:text-emerald-400 transition duration-200"
            >
              Contact
            </a>
          </li>
        </ul>

        {/* Mobile Toggle */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="md:hidden focus:outline-none"
        >
          {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <ul className="md:hidden mt-4 space-y-2 text-sm font-medium text-center">
          <li>
            <a
              href="#"
              className="block hover:text-emerald-400 transition duration-200"
            >
              Home
            </a>
          </li>
          <li>
            <a
              href="#"
              className="block hover:text-emerald-400 transition duration-200"
            >
              About
            </a>
          </li>
          <li>
            <a
              href="#"
              className="block hover:text-emerald-400 transition duration-200"
            >
              Contact
            </a>
          </li>
        </ul>
      )}
    </nav>
  );
}
