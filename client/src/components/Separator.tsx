export default function Separator({
  type,
}: {
  type: "vertical" | "horizontal";
}) {
  const isVertical = type === "vertical";

  return (
    <div
      className={`${
        isVertical ? "w-[1px] h-auto" : "w-full h-[1px] my-2"
      } bg-gray-300`}
    ></div>
  );
}
