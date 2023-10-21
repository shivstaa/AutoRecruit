import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Profile() {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [jobDescription, setJobDescription] = useState('');
    const [companyName, setCompanyName] = useState('');
    const [file, setFile] = useState(null);
    const [errors, setErrors] = useState({});

    const navigate = useNavigate();

    const onFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile && selectedFile.type === "application/pdf") {
            setFile(selectedFile);
        } else {
            setFile(null);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        let formErrors = {};
        if (!file) formErrors.file = "Please upload a PDF file.";
        if (!firstName.trim()) formErrors.firstName = "First name is required.";
        if (!lastName.trim()) formErrors.lastName = "Last name is required.";
        if (!jobDescription.trim()) formErrors.jobDescription = "Job description is required.";

        setErrors(formErrors);

        if (Object.keys(formErrors).length === 0) {
            navigate('/interview');
        }
    };

    return (
        <main className="min-h-screen bg-gray-900 text-gray-300 p-4 flex justify-center items-center">
            <div style={{ width: '40vw', height: '75vh' }} className="bg-gray-800 p-4 rounded shadow-lg">
                <form onSubmit={handleSubmit}>
                    <div className="mb-4">
                        <label className="block text-sm font-medium">Upload PDF</label>
                        <input type="file" onChange={onFileChange} className="mt-2 bg-gray-700 border border-gray-600 text-gray-300 rounded" />
                        {errors.file && <p className="text-red-500 text-xs mt-1">{errors.file}</p>}
                    </div>

                    <div className="flex gap-4 mb-4">
                        <div className="flex-1">
                            <label className="block text-sm font-medium">First Name</label>
                            <input value={firstName} onChange={(e) => setFirstName(e.target.value)} className="mt-2 p-2 w-full bg-gray-700 border border-gray-600 text-gray-300 rounded" />
                            {errors.firstName && <p className="text-red-500 text-xs mt-1">{errors.firstName}</p>}
                        </div>

                        <div className="flex-1">
                            <label className="block text-sm font-medium">Last Name</label>
                            <input value={lastName} onChange={(e) => setLastName(e.target.value)} className="mt-2 p-2 w-full bg-gray-700 border border-gray-600 text-gray-300 rounded" />
                            {errors.lastName && <p className="text-red-500 text-xs mt-1">{errors.lastName}</p>}
                        </div>
                    </div>

                    <div className="mb-4">
                        <label className="block text-sm font-medium">Job Description</label>
                        <input value={jobDescription} onChange={(e) => setJobDescription(e.target.value)} className="mt-2 p-2 w-full bg-gray-700 border border-gray-600 text-gray-300 rounded" />
                        {errors.jobDescription && <p className="text-red-500 text-xs mt-1">{errors.jobDescription}</p>}
                    </div>

                    <div className="mb-4 w-1/2">
                        <label className="block text-sm font-medium">Company Name</label>
                        <input value={companyName} onChange={(e) => setCompanyName(e.target.value)} className="mt-2 p-2 w-full bg-gray-700 border border-gray-600 text-gray-300 rounded" />
                    </div>

                    <button type="submit" className="bg-blue-500 text-gray-900 px-4 py-2 rounded hover:bg-blue-600">Submit</button>
                </form>
            </div>
        </main>
    )
}

export default Profile;
