import React, { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

const ProductSection = () => {
  const [products, setProducts] = useState([]);
  React.useEffect(() => {
    axios
      .get("/api/getProducts")
      .then((res) => setProducts(res.data))
      .catch((error) => console.error(error));
  }, []);

  const limitedProducts = [
    {
      img: "https://nobero.com/cdn/shop/files/17_f42434b2-ce4b-4f60-9f25-716ec028b8d9.jpg?v=1712051278&width=1066",
      name: "Kurta",
      price: 500,
      id: 1,
    },
    {
      img: "https://nobero.com/cdn/shop/files/17_f42434b2-ce4b-4f60-9f25-716ec028b8d9.jpg?v=1712051278&width=1066",
      name: "Kurta",
      price: 500,
      id: 2,
    },
    {
      img: "https://nobero.com/cdn/shop/files/17_f42434b2-ce4b-4f60-9f25-716ec028b8d9.jpg?v=1712051278&width=1066",
      name: "Kurta",
      price: 500,
      id: 3,
    },
  ];

  return (
    <>
      <div className="p-7 h-auto w-full box-border flex justify-between items-center flex-wrap">
        {limitedProducts.map((items) => (
          <div
            className="cards h-64 w-48 md:h-80 md:w-64 lg:h-96 lg:w-80 p-5 mt-2 rounded-lg"
            key={items.id}
          >
            <Link to={`/ProductDescription/${items.id}`}>
              <div>
                <img
                  className="rounded-lg h-36 md:h-48 lg:h-64 w-full bg-slate-600 mb-5 object-cover"
                  src={items.img}
                  alt="img"
                />
              </div>
            </Link>

            <h2 className="poppins">{items.name}</h2>
            <h3>{items.price}</h3>
          </div>
        ))}
      </div>
    </>
  );
};

export default ProductSection;
