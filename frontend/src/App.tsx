import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

function App() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 p-8">
      <h1 className="text-5xl font-extrabold tracking-tight text-center text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 animate-pulse">
        StockSense
      </h1>
      <p className="text-center text-gray-400 mt-4 text-lg">
        Your stock portfolio at a glance
      </p>
      <Separator className="my-8 w-3/4 bg-gray-700" />
      <Button className="relative group px-8 py-4 text-xl font-medium text-white bg-indigo-600 rounded-lg shadow-lg transition-all transform hover:scale-105 hover:shadow-2xl focus:outline-none focus:ring-4 focus:ring-indigo-400">
        <span className="absolute inset-0 transition-transform transform bg-gradient-to-r from-purple-500 to-pink-500 opacity-0 group-hover:opacity-100 group-hover:scale-110 rounded-lg"></span>
        <span className="relative">View Dashboard</span>
      </Button>
    </div>
  );
}

export default App;