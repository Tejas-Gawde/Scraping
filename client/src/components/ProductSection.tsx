import { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

// Define interfaces for product and API response
interface Product {
  title: string;
  product_urls: { imgurl: string }[];
  price: string;
}

interface ApiResponse {
  products: Product[];
}

const ProductSection: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get<ApiResponse>(
          "http://127.0.0.1:8000/api/getproducts"
        );
        setProducts(response.data.products);
        console.log(response.data.products);
      } catch (error) {
        console.error("Error fetching products:", error);
        setError("Failed to load products.");
      }
    };
    fetchProducts();
  }, []);

  return (
    <div className="p-7 h-auto w-full box-border flex flex-wrap justify-between items-center">
      {error && <p className="text-red-500">{error}</p>}
      {products.length === 0 ? (
        <p>Loading...</p>
      ) : (
        products.map((item) => (
          <div
            className="card h-64 w-48 md:h-80 md:w-64 lg:h-96 lg:w-80 p-5 mt-2 rounded-lg shadow-md"
            key={item.title}
          >
            <Link to={`/ProductDescription/${item.title.replace(/\s+/g, "-")}`}>
              <div>
                <img
                  className="rounded-lg h-36 md:h-48 lg:h-64 w-full bg-slate-600 mb-5 object-cover"
                  src={item.product_urls[0].imgurl}
                  alt={item.title}
                />
              </div>
            </Link>
            <Link to={`/ProductDescription/${item.title.replace(/\s+/g, "-")}`}>
              <h2 className="text-lg font-semibold poppins transition-colors hover:text-blue-500">
                {item.title}
              </h2>
            </Link>
            <h3 className="text-md text-gray-700 py-2">{item.price}</h3>
          </div>
        ))
      )}
    </div>
  );
};

export default ProductSection;
