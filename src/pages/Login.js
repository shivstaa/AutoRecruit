import React, { useState } from 'react';
import { AiOutlineMail, AiOutlineUser, AiOutlineLock, AiOutlineEye, AiOutlineEyeInvisible } from 'react-icons/ai';

function Login() {
    const [showPassword, setShowPassword] = useState(false);
    const [isLogin, setIsLogin] = useState(true);

    return (
        <main className="min-h-screen flex items-center justify-center bg-gray-900">
            <div className="p-10 bg-gray-800 text-white rounded-lg shadow-md w-[30vw] h-[75vh] flex flex-col">
                
                <div className="flex items-center justify-center mb-4 space-x-6 relative">
                    <h1 className={`text-xl font-bold cursor-pointer ${isLogin ? 'bg-gray-700 shadow-md' : 'text-opacity-50'}`} onClick={() => setIsLogin(true)}>Login</h1>
                    <div className="border-r border-white h-5"></div>
                    <h1 className={`text-xl font-bold cursor-pointer ${!isLogin ? 'bg-gray-700 shadow-md' : 'text-opacity-50'}`} onClick={() => setIsLogin(false)}>Sign Up</h1>
                </div>
                
                <div className="w-2/3 mx-auto h-px bg-white mb-6"></div>

                { !isLogin && 
                    <div className='mb-4 relative'>
                        <AiOutlineMail className='absolute top-3 left-3'/>
                        <input required className='pl-10 pr-4 py-2 rounded-lg bg-gray-700 w-full mb-4' placeholder='Email' type='email' />
                    </div>
                }

                <div className='mb-4 relative'>
                    <AiOutlineUser className='absolute top-3 left-3'/>
                    <input required className='pl-10 pr-4 py-2 rounded-lg bg-gray-700 w-full mb-4' placeholder='Username' />
                </div>
                
                <div className='mb-4 relative'>
                    <AiOutlineLock className='absolute top-3 left-3'/>
                    <input required className='pl-10 pr-4 py-2 rounded-lg bg-gray-700 w-full mb-4' placeholder='Password' type={showPassword ? 'text' : 'password'} />
                    <button className='absolute top-3 right-3' onClick={() => setShowPassword(!showPassword)}>
                        { showPassword ? <AiOutlineEyeInvisible /> : <AiOutlineEye /> }
                    </button>
                </div>
                
                { isLogin ?
                    <>
                        <button className="w-full py-2 rounded-lg bg-purple-600 text-white font-bold mb-4">Login</button>
                        <div className="text-right mb-6">
                            <a href="#" className="text-sm text-gray-300 hover:underline">Lost Password? Click Here!</a>
                        </div>
                    </>
                    :
                    <button className="w-full py-2 rounded-lg bg-purple-600 text-white font-bold mb-4">Sign Up</button>
                }
            </div>
        </main>
    )
}

export default Login;
