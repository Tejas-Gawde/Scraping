import "./App.css";
import Homepage from "./pages/Homepage";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import ProductPage from "./pages/ProductPage";

const App = () => {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route
            path="/ProductDescription/:productName"
            element={<ProductPage />}
          />
        </Routes>
      </Router>
    </>
  );
};

export default App;
