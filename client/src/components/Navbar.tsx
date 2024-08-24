import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCartShopping } from "@fortawesome/free-solid-svg-icons";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <>
      <div className="h-12 lg:h-16 w-full box-border flex justify-between items-center pl-4 pr-4">
        <div className="heading text-xl lg:text-3xl md:text-2xl font-bold italic text-gray-600">
          <Link to="/">Nobero</Link>
        </div>
        <div className="hidden md:flex md:gap-5">
          <Link className="hover:text-blue-600 transition-colors" to="/">
            Home
          </Link>
          <Link className="hover:text-blue-600 transition-colors" to="/admin">
            Admin
          </Link>
          <Link className="hover:text-blue-600 transition-colors" to="/contact">
            Contact
          </Link>
          <Link className="hover:text-blue-600 transition-colors" to="/product">
            Product
          </Link>
        </div>
        <div className="flex items-center justify-center">
          <button className="border-2 lg:text-xl text-sm p-1 lg:p-2 w-16 lg:w-24 rounded-3xl mr-4 hover:bg-green-800 hover:text-white">
            <Link to="/login">Login</Link>
          </button>
          <button
            onClick={() => {
              document.body.style.overflowY = "hidden";
            }}
          >
            <FontAwesomeIcon icon={faCartShopping} size="2xl" />
            <span className="ml-1">10</span>
          </button>
        </div>
      </div>
    </>
  );
};

export default Navbar;
