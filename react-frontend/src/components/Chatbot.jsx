import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BiChat } from 'react-icons/bi';

function Chatbot() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([
        {
            sender: 'bot', text: "👋 Welcome to FinRAG — your AI-powered financial assistant!  Ask me anything about investments, market trends, real estate, RRSPs, cryptocurrencies, or the Edmonton economy. I’ll give you fast, clear, and reliable answers based on trusted data.Let’s get started!"
        }
    ]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const inputRef = useRef(null);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages, isTyping]);

    useEffect(() => {
        if (isOpen && inputRef.current) {
            inputRef.current.focus();
        }
    }, [isOpen]);

    const handleSend = async (e) => {
        e.preventDefault();
        const query = input.trim();
        if (!query) return;

        setMessages(prev => [...prev, { sender: 'user', text: query }]);
        setInput('');
        setIsTyping(true);

        try {
            const response = await fetch('http://localhost:8000/chat/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });

            if (!response.ok) throw new Error('API request failed');
            const data = await response.json();
            const fullAnswer = data.response || "No answer received.";

            let displayed = '';
            for (let i = 0; i < fullAnswer.length; i++) {
                displayed += fullAnswer[i];
                setMessages(prev => {
                    const last = prev.at(-1);
                    if (last?.sender === 'bot' && last.typing) {
                        return [...prev.slice(0, -1), { sender: 'bot', text: displayed, typing: true }];
                    } else {
                        return [...prev, { sender: 'bot', text: displayed, typing: true }];
                    }
                });
                await new Promise(res => setTimeout(res, 15));
            }

            setMessages(prev =>
                prev.map(msg => msg.typing ? { ...msg, typing: false } : msg)
            );

        } catch (error) {
            setMessages(prev => [...prev, { sender: 'bot', text: "Sorry, there was an error processing your request." }]);
            console.error(error);
        } finally {
            setIsTyping(false);
        }
    };

    return (
        <div>
            {/* Floating Chat Icon */}
            {!isOpen && (
                <button
                    onClick={() => setIsOpen(true)}
                    className="fixed bottom-6 right-6 w-14 h-14 bg-blue-600 hover:bg-blue-700 text-white rounded-full flex items-center justify-center shadow-lg transition-all duration-200 z-[9999]"
                >
                    <BiChat className="text-2xl" />
                </button>
            )}

            {/* Chat Modal */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-[9999]"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                    >
                        <motion.div
                            className="bg-gray-900 text-white rounded-xl shadow-2xl flex flex-col w-full max-w-md h-[600px]"
                            initial={{ scale: 0.95, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.95, opacity: 0 }}
                            transition={{ type: 'spring', stiffness: 200, damping: 20 }}
                        >
                            {/* Header */}
                            <div className="bg-blue-600 text-white px-4 py-3 rounded-t-xl flex items-center justify-between">
                                <h3 className="font-semibold text-lg">Finance Assistant</h3>
                                <button onClick={() => setIsOpen(false)} className="text-2xl leading-none hover:text-gray-300">
                                    &times;
                                </button>
                            </div>

                            {/* Chat Messages */}
                            <div className="flex-1 p-4 overflow-y-auto space-y-3 bg-gray-800">
                                {messages.map((msg, idx) => (
                                    <div
                                        key={idx}
                                        className={`max-w-[85%] px-4 py-2 rounded-lg text-sm ${msg.sender === 'user'
                                            ? 'bg-blue-600 text-white self-end ml-auto rounded-br-none'
                                            : 'bg-gray-700 text-gray-100 self-start mr-auto rounded-bl-none'
                                            }`}
                                    >
                                        {msg.text}
                                    </div>
                                ))}
                                {isTyping && (
                                    <div className="text-xs italic text-gray-400">Bot is typing...</div>
                                )}
                                <div ref={messagesEndRef} />
                            </div>

                            {/* Input */}
                            <form onSubmit={handleSend} className="px-4 py-3 bg-gray-900 border-t border-gray-700 flex space-x-2">
                                <input
                                    type="text"
                                    ref={inputRef}
                                    className="flex-1 px-4 py-2 rounded-full bg-gray-700 border border-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                                    placeholder="Ask a financial question..."
                                    value={input}
                                    onChange={(e) => setInput(e.target.value)}
                                />
                                <button
                                    type="submit"
                                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm rounded-full transition-all duration-200"
                                >
                                    Send
                                </button>
                            </form>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}

export default Chatbot;
