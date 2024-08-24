import Navbar from "../components/Navbar";
import { useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";

const ProdDesc = () => {
  const [number, setnumber] = useState(1);
  const location = useLocation();
  const route = location.pathname;

  // Assuming you have a function to fetch product details by id
  const getProductDetails = async (route: string) => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api${route}`);
      return response.data;
    } catch (error) {
      console.error(error);
    }
  };
  const [product, setProduct] = useState(null);

  useEffect(() => {
    getProductDetails(route).then((data) => setProduct(data));
    window.scrollTo(0, 0);
    setnumber(1);
  }, [route]);

  return (
    <>
      <div className="Main-prod-body w-full">
        <Navbar />
        <div className="product-section h-1/2 w-11/12 flex p-5 lg:p-12">
          <div className="md:w-1/3 w-1/2 lg:w-1/4 bg-slate-200">
            <img
              className="size-[400px] object-cover"
              src={product?.product_urls[0].imgurl}
              alt={product?.title}
            />
          </div>
          <div className="w-1/2 lg:w-3/4 ml-5">
            <h1 className="text-xl md:text-2xl lg:text-4xl font-bold">
              {product?.title}
            </h1>
            <h4 className="text-lg lg:text-xl font-medium">Details : </h4>
            <p className="text-sm md:text-sm lg:text-lg poppins">
              {product?.description}
            </p>
            <br className="hidden lg:block"></br>
            <h1 className="text-lg lg:text-2xl font-bold">₹{product?.price}</h1>
            <div className="Quantity flex text-2xl items-center">
              <h1 className="mr-3 text-lg">Quantity : </h1>
              <button
                className="h-7 w-10 flex justify-center items-center mr-2"
                onClick={() => {
                  setnumber((number) => number + 1);
                }}
              >
                +
              </button>
              <h1 className="mr-2 text-lg">{number}</h1>
              <button
                className="h-7 w-10 flex justify-center items-center mr-2"
                onClick={() => {
                  number > 1 && setnumber((number) => number - 1);
                }}
              >
                -
              </button>
            </div>
            <div className="button flex mt-3">
              <button className="h-10 w-40  mr-4 border-2  border-red-600 text-red-600">
                Add to cart
              </button>
              <button className="h-10 w-40 bg-red-600 text-white mr-4">
                Buy Now
              </button>
            </div>
          </div>
        </div>

        <div>
          <h1 className="text-center font-medium text-3xl mt-4 tracking-wide">
            You may also like...
          </h1>
        </div>
      </div>
    </>
  );
};

export default ProdDesc;
