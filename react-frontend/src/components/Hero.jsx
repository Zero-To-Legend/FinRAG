import React from 'react';
import { motion } from 'framer-motion';

function Hero({ onChatClick }) {
    return (
        <motion.section
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="min-h-[calc(100vh-128px)] bg-gray-900 text-white flex flex-col md:flex-row items-center justify-between px-6 md:px-12 py-8 z-10 relative"
        >
            {/* Left Content */}
            <div className="md:w-1/2 text-center md:text-left">
                <h1 className="text-4xl md:text-5xl font-extrabold leading-tight mb-6">
                    Smarter Insights, <br className="hidden md:block" />
                    Better Decisions — <br />
                    For Every Financial Journey.
                </h1>
                <p className="text-lg text-gray-300 mb-4">
                    From budgets to investments, make every dollar count <br />
                    with our intelligent financial assistant.
                </p>
                <p className="text-lg text-gray-400 mb-6">
                    How will you spend your <span className="line-through text-red-400">money</span> life?
                </p>
                <button
                    onClick={onChatClick}
                    className="inline-block px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded transition-colors duration-200"
                >
                    Click the Chat button on the bottom right to Start
                </button>
            </div>

            {/* Right Image */}
            <div className="md:w-1/2 flex justify-center md:justify-end mt-10 md:mt-0">
                <img
                    src="https://images.pexels.com/photos/6969625/pexels-photo-6969625.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
                    alt="Banking illustration"
                    className="w-full max-w-sm rounded-xl shadow-lg"
                />
            </div>
        </motion.section>
    );
}

export default Hero;
