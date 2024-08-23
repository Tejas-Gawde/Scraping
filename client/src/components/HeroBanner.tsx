import model from "../assets/Model.png";

const HeroBanner = () => {
  return (
    <div className="w-full h-60 lg:h-96 bg-gray-800 flex justify-between items-center text-white px-7 lg:px-24 lg:mb-12">
      <div className="flex flex-col justify-center items-start">
        <h1 className="text-3xl lg:text-7xl md:text-5xl font-bold mb-8">
          Discover Your Style
        </h1>
        <p className="text-md lg:text-xl mb-4">
          Explore our latest collection and find your perfect fit.
        </p>
        <button className="bg-white text-xs md:text-sm lg-text-lg text-gray-800 font-bold py-2 px-2 lg:py-2 lg:px-6 rounded-3xl   hover:bg-gray-500 hover:text-white transition duration-300 ease-in-out">
          Shop Now
        </button>
      </div>
      <div className="h-full w-2/5">
        <img className="object-cover h-full w-full" src={model} alt="Model" />
      </div>
    </div>
  );
};

export default HeroBanner;
