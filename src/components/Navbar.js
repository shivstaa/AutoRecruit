import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-blue-500 p-4 text-white">
      <ul className="flex space-x-4">
        <li>
          <Link to="/" className="hover:underline">Home</Link>
        </li>
        <li>
          <Link to="/login" className="hover:underline">Login</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
