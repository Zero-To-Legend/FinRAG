import React, { useState, useRef, useEffect } from 'react';
import Logo from '../assets/logo.svg';
import {
    FaRobot,
    FaMoneyCheckAlt,
    FaRegChartBar,
    FaBars,
    FaTimes,
    FaChevronDown,
    FaHome,
} from 'react-icons/fa';

const navItems = [
    {
        label: 'Chat Assistant',
        icon: <FaRobot />,
        subItems: ['Ask a Question', 'Popular Topics', 'AI Capabilities'],
    },
    {
        label: 'Financial Tools',
        icon: <FaMoneyCheckAlt />,
        subItems: ['Investment Tracker', 'Real Estate Trends', 'Tax Survey Insights'],
    },
    {
        label: 'Analytics',
        icon: <FaRegChartBar />,
        subItems: ['Spending Breakdown', 'Property Assessment Insights', 'Market Stats'],
    },
];

const infoContent = {
    'Ask a Question': 'Type any finance-related query—whether it’s about stocks, taxes, real estate, or crypto. FinRAG uses real-time data and GPT intelligence to give you clear, accurate answers.',
    'Popular Topics': 'Explore topics like crypto safety, RRSP planning, inflation, Edmonton real estate trends, and investment diversification. These are questions we answer best!',
    'AI Capabilities': 'FinRAG uses Retrieval-Augmented Generation (RAG) combined with GPT-3.5 to deliver localized, data-backed financial responses focused on the Edmonton region and broader financial topics.',
    'Investment Tracker': 'Compare your investments—stocks, bonds, ETFs, or crypto—against inflation trends and financial benchmarks using live insights.',
    'Real Estate Trends': 'Analyze how Edmonton’s housing market is performing. We provide updates from public records including pricing trends and growth comparisons.',
    'Tax Survey Insights': 'Gain insight into how Edmonton residents view public taxes and services, based on annual city-wide perception surveys and expenditure reports.',
    'Spending Breakdown': 'Explore average household spending habits in Edmonton—from rent and groceries to entertainment and savings—based on open municipal datasets.',
    'Property Assessment Insights': 'Learn how the City of Edmonton assesses property values and what affects your assessed value over time.',
    'Market Stats': 'Access financial data such as executive-level public spending, budget allocation reports, and macroeconomic stats for Alberta and beyond.',
    'About FinRAG': 'FinRAG is an AI-powered financial assistant developed as part of the MM802 Multimedia Communications project by Ruban Gino Singh A, Raja Priya M, and Raju B. It provides personalized financial insights powered by GPT and Edmonton Open Data.'
};


export default function Navbar() {
    const [mobileOpen, setMobileOpen] = useState(false);
    const [activeDropdown, setActiveDropdown] = useState(null);
    const [selectedInfo, setSelectedInfo] = useState(null);
    const dropdownRef = useRef(null);

    const toggleDropdown = (label) => {
        setActiveDropdown(activeDropdown === label ? null : label);
    };

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setActiveDropdown(null);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    return (
        <nav className="bg-gray-900 text-white w-full fixed top-0">
            <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
                {/* Logo */}
                <div className="flex items-center space-x-2">
                    <img src={Logo} alt="Logo" className="h-10" />
                    <span className="text-2xl font-bold">FinRAG</span>
                </div>

                {/* Desktop Navigation */}
                <div className="hidden lg:flex items-center space-x-8" ref={dropdownRef}>
                    <button
                        onClick={() => setSelectedInfo('About FinRAG')}
                        className="flex items-center space-x-1 hover:text-blue-400"
                    >
                        <FaHome />
                        <span>Home</span>
                    </button>

                    {navItems.map((item) => (
                        <div key={item.label} className="relative">
                            <button
                                onClick={() => toggleDropdown(item.label)}
                                className="flex items-center space-x-1 hover:text-blue-400"
                            >
                                {item.icon}
                                <span>{item.label}</span>
                                <FaChevronDown className="text-xs" />
                            </button>

                            {activeDropdown === item.label && (
                                <div className="absolute top-full mt-2 bg-gray-800 rounded shadow-lg py-2 z-50 min-w-max">
                                    {item.subItems.map((sub) => (
                                        <button
                                            key={sub}
                                            onClick={() => setSelectedInfo(sub)}
                                            className="block w-full px-4 py-2 hover:bg-gray-700 text-right"
                                        >
                                            {sub}
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>
                    ))}
                </div>

                {/* Mobile Toggle */}
                <div className="lg:hidden flex items-center">
                    <button onClick={() => setMobileOpen(!mobileOpen)} className="ml-auto">
                        {mobileOpen ? <FaTimes size={22} /> : <FaBars size={22} />}
                    </button>
                </div>
            </div>

            {/* Mobile Navigation */}
            {mobileOpen && (
                <div className="lg:hidden bg-gray-800 px-4 py-4 space-y-6">
                    <div>
                        <div className="font-semibold flex items-center space-x-2">
                            <FaHome />
                            <span>Home</span>
                        </div>
                        <button
                            className="mt-2 text-sm text-right w-full hover:text-blue-400"
                            onClick={() => {
                                setSelectedInfo('About FinRAG');
                                setMobileOpen(false);
                            }}
                        >
                            About FinRAG
                        </button>
                    </div>

                    {navItems.map((item) => (
                        <div key={item.label}>
                            <div className="font-semibold flex items-center space-x-2">
                                {item.icon}
                                <span>{item.label}</span>
                            </div>
                            <div className="mt-2 text-right">
                                {item.subItems.map((sub) => (
                                    <button
                                        key={sub}
                                        onClick={() => {
                                            setSelectedInfo(sub);
                                            setMobileOpen(false);
                                        }}
                                        className="block w-full py-1 text-gray-300 hover:text-white text-right"
                                    >
                                        {sub}
                                    </button>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Info Modal */}
            {selectedInfo && (
                <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex justify-center items-center px-4">
                    <div className="bg-gray-800 text-white rounded-lg shadow-xl w-full max-w-md p-6 relative">
                        <button
                            onClick={() => setSelectedInfo(null)}
                            className="absolute top-2 right-4 text-2xl text-gray-300 hover:text-white"
                        >
                            &times;
                        </button>
                        <h2 className="text-2xl font-bold mb-4">{selectedInfo}</h2>
                        <p className="text-gray-300">{infoContent[selectedInfo]}</p>
                    </div>
                </div>
            )}
        </nav>
    );
}
