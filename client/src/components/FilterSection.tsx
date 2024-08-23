import React, { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { ChevronDown, ChevronUp } from "lucide-react";

type FilterOption = {
  label: string;
  value: string;
  color?: string;
};

type FilterSection = {
  title: string;
  options: FilterOption[];
  type: "single" | "multiple";
};

const filterSections: FilterSection[] = [
  {
    title: "Price",
    type: "single",
    options: [
      { label: "₹0 - ₹500", value: "0-500" },
      { label: "₹500 - ₹1000", value: "500-1000" },
      { label: "₹1000 - ₹1500", value: "1000-1500" },
      { label: "₹1500 - ₹2000", value: "1500-2000" },
      { label: "₹2000 - ₹2500", value: "2000-2500" },
    ],
  },
  {
    title: "Color",
    type: "multiple",
    options: [
      { label: "Aloe Green", value: "aloe-green", color: "#98FB98" },
      { label: "Apricot Crush", value: "apricot-crush", color: "#FBCEB1" },
      { label: "Authentic/ Never Say No", value: "authentic" },
      { label: "Be Free/ Believe", value: "be-free" },
      { label: "Black", value: "black", color: "#000000" },
    ],
  },
  {
    title: "Size",
    type: "multiple",
    options: [
      { label: "S", value: "s" },
      { label: "M", value: "m" },
      { label: "L", value: "l" },
      { label: "XL", value: "xl" },
    ],
  },
];

const FilterColumn: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [expandedSections, setExpandedSections] = useState<string[]>(["Color"]);

  const toggleSection = (title: string) => {
    setExpandedSections((prev) =>
      prev.includes(title) ? prev.filter((t) => t !== title) : [...prev, title]
    );
  };

  const toggleFilter = (section: FilterSection, value: string) => {
    const currentParams = new URLSearchParams(searchParams);
    const currentValues = currentParams.getAll(section.title.toLowerCase());

    if (section.type === "single") {
      if (currentValues[0] === value) {
        currentParams.delete(section.title.toLowerCase());
      } else {
        currentParams.set(section.title.toLowerCase(), value);
      }
    } else {
      if (currentValues.includes(value)) {
        const newValues = currentValues.filter((v) => v !== value);
        currentParams.delete(section.title.toLowerCase());
        newValues.forEach((v) =>
          currentParams.append(section.title.toLowerCase(), v)
        );
      } else {
        currentParams.append(section.title.toLowerCase(), value);
      }
    }

    setSearchParams(currentParams);
  };

  const clearAll = () => {
    setSearchParams(new URLSearchParams());
  };

  const isSelected = (section: FilterSection, value: string) => {
    const currentValues = searchParams.getAll(section.title.toLowerCase());
    return currentValues.includes(value);
  };

  return (
    <div className="w-64 bg-white shadow-md rounded-lg p-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">Filter</h2>
        <button onClick={clearAll} className="text-yellow-600 hover:underline">
          Clear All
        </button>
      </div>
      {filterSections.map((section) => (
        <div key={section.title} className="mb-4">
          <button
            className="flex justify-between items-center w-full text-left font-medium"
            onClick={() => toggleSection(section.title)}
          >
            {section.title}
            {expandedSections.includes(section.title) ? (
              <ChevronUp size={20} />
            ) : (
              <ChevronDown size={20} />
            )}
          </button>
          <div
            className={`mt-2 space-y-2 overflow-hidden transition-all duration-300 ease-in-out ${
              expandedSections.includes(section.title)
                ? "max-h-96 opacity-100"
                : "max-h-0 opacity-0"
            }`}
          >
            {section.options.map((option) => (
              <label key={option.value} className="flex items-center space-x-2">
                <input
                  type={section.type === "single" ? "radio" : "checkbox"}
                  checked={isSelected(section, option.value)}
                  onChange={() => toggleFilter(section, option.value)}
                  className={`${
                    section.type === "single" ? "form-radio" : "form-checkbox"
                  } h-4 w-4 text-yellow-600`}
                  name={section.title}
                />
                <span className="flex items-center">
                  {option.color && (
                    <span
                      className="w-4 h-4 rounded-full inline-block mr-2"
                      style={{ backgroundColor: option.color }}
                    />
                  )}
                  {option.label}
                </span>
              </label>
            ))}
          </div>
        </div>
      ))}
      <button className="mt-4 w-full bg-yellow-600 text-white py-2 rounded-md hover:bg-yellow-700">
        Show
      </button>
    </div>
  );
};

export default FilterColumn;
