import Navbar from "../components/Navbar";
import HeroBanner from "../components/HeroBanner";
import ProductSection from "../components/ProductSection";
import { Link } from "react-router-dom";
import FilterSection from "../components/FilterSection";
import Separator from "../components/Separator";

const Homepage = () => {
  return (
    <>
      <div className="h-full w-full flex flex-col items-center">
        <Navbar />
        <HeroBanner />
        <h1 className="text-center font-semibold text-2xl  lg:text-4xl mt-4 tracking-wide poppins">
          Featured Products
        </h1>
        <div className="flex w-11/12 ">
          <FilterSection />
          <Separator type="vertical" />
          <ProductSection />
        </div>

        <div className="flex justify-center">
          <Link to="/product">
            <button className="border-2 p-2 w-40 rounded-3xl">See More</button>
          </Link>
        </div>
      </div>
    </>
  );
};

export default Homepage;
