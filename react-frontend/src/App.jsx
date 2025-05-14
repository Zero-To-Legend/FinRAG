import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Chatbot from './components/Chatbot';
import Footer from './components/Footer';

function App() {
  const [isChatOpen, setIsChatOpen] = useState(false);

  return (
    <div className="bg-gray-900 text-gray-100 min-h-screen">
      {/* Navbar stays fixed on top */}
      <Navbar />

      {/* Add margin-top to offset fixed navbar height (assume ~64px) */}
      <div className="pt-20">
        {/* Hero Section */}
        <header className="w-full bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900">
          <div className="max-w-7xl mx-auto px-4">
            <Hero onChatClick={() => setIsChatOpen(true)} />
          </div>
        </header>

        {/* Chatbot with open/close state */}
        <Chatbot isOpen={isChatOpen} setIsOpen={setIsChatOpen} />

        <Footer />
      </div>
    </div>
  );
}

export default App;
