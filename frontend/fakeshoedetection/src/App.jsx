import Navbar from "./components/NavBar";
import Footer from "./components/Footer";
import ImageUploader from "./components/ImageLoader";
import { Toaster } from "react-hot-toast";

function App() {
  return (
    <div className="bg-gray-900 min-h-screen text-gray-100 flex flex-col">
      <Toaster />
      <Navbar />
      <main className="flex-grow flex items-center justify-center">
        <ImageUploader />
      </main>
      <Footer />
    </div>
  );
}

export default App;
