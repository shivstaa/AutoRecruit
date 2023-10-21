import React, { useState } from 'react';
import { AiOutlineMail, AiOutlineUser, AiOutlineLock, AiOutlineEye, AiOutlineEyeInvisible } from 'react-icons/ai';

function Login() {
    const [showPassword, setShowPassword] = useState(false);
    const [isLogin, setIsLogin] = useState(true);
    const [notification, setNotification] = useState(null);

    const handleSubmit = () => {
        // Validate inputs
        const inputs = document.querySelectorAll('input[required]');
        let valid = true;

        inputs.forEach(input => {
            if (!input.value) valid = false;
        });

        if (!valid) {
            alert('Please fill in all required fields.');
            return;
        }

        // Placeholder for further processing like API calls, etc.
        console.log('Submission successful.');
    };

    const handleForgotPassword = () => {
        const email = prompt("Please enter your email:");
        if (email) {
            // Here, you can make an API call to handle the password reset logic.
            setNotification("Email sent successfully!");
            setTimeout(() => setNotification(null), 2000); // Hide after 2 seconds
        }
    };

    return (
        <main className="min-h-screen flex items-center justify-center bg-gray-900">
            {notification && (
                <div className="fixed top-0 left-0 w-full p-4 text-center bg-green-500 text-white">
                    {notification}
                </div>
            )}
            <div className="p-10 bg-gray-800 text-white rounded-lg shadow-md w-[30vw] h-[70 vh] flex flex-col">
                
                <div className="flex items-center justify-center mb-4 space-x-6 relative">
                    <h1 className={`text-xl font-bold cursor-pointer ${isLogin ? 'bg-gray-700 shadow-md' : 'text-opacity-50'}`} onClick={() => setIsLogin(true)}>Login</h1>
                    <div className="border-r border-white h-5"></div>
                    <h1 className={`text-xl font-bold cursor-pointer ${!isLogin ? 'bg-gray-700 shadow-md' : 'text-opacity-50'}`} onClick={() => setIsLogin(false)}>Sign Up</h1>
                </div>
                
                <div className="w-2/3 mx-auto h-px bg-white mb-6"></div>

                { !isLogin && 
                <div>
                <label className="block mb-1">Email:</label>
                    <div className='mb-4 relative'>
                        <AiOutlineMail className='absolute top-3 left-3'/>
                        <input required className='pl-10 pr-4 py-2 rounded-lg bg-gray-700 w-full mb-4' placeholder='Email' type='email' />
                    </div>
                </div>
                }
                    <label className="block mb-1">Username:</label>

                <div className='mb-4 relative'>
                    <AiOutlineUser className='absolute top-3 left-3'/>
                    <input required className='pl-10 pr-4 py-2 rounded-lg bg-gray-700 w-full mb-4' placeholder='Username' />
                </div>
                
                <label className="block mb-1">Password:</label>
                <div className='mb-4 relative'>
                    <AiOutlineLock className='absolute top-3 left-3'/>
                    <input required className='pl-10 pr-4 py-2 rounded-lg bg-gray-700 w-full mb-4' placeholder='Password' type={showPassword ? 'text' : 'password'} />
                    <button className='absolute top-3 right-3' onClick={() => setShowPassword(!showPassword)}>
                        { showPassword ? <AiOutlineEyeInvisible /> : <AiOutlineEye /> }
                    </button>
                </div>
                
                { isLogin ?
                    <>
                        <button onClick={handleSubmit} className="w-full py-2 rounded-lg bg-purple-600 text-white font-bold mb-4">Login</button>
                        <div className="text-right mb-6">
                            <a href="#" onClick={handleForgotPassword} className="text-sm text-center text-gray-300 hover:underline">Lost Password? Click Here!</a>
                        </div>
                    </>
                    :
                    <button onClick={handleSubmit} className="w-full py-2 rounded-lg bg-purple-600 text-white font-bold mb-4">Sign Up</button>
                }
            </div>
        </main>
    )
}

export default Login;
