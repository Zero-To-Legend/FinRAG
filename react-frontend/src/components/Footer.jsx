import React from 'react';

function Footer() {
    return (
        <footer className="z-20 fixed bottom-0 left-0 w-full bg-gray-900 text-gray-400 border-t border-gray-700 py-2">
            <div className="max-w-7xl mx-auto px-4 py-4 flex justify-center items-center text-center">
                <p className="text-sm">
                    &copy; {new Date().getFullYear()} All rights reserved | Developed by
                    <span className="text-white font-medium"> Ruban Gino Singh, Raja Priya, & Raju</span>
                </p>
            </div>
        </footer>
    );
}

export default Footer;
