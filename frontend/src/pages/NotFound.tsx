import React from "react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export const NotFound: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 p-8">
      <h1 className="text-5xl font-extrabold tracking-tight text-center text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 animate-pulse">
        Oops!
      </h1>
      <p className="mt-4 text-lg text-center text-gray-400">
        Something went wrong. We couldn't find the page you're looking for.
      </p>
      <Button
        onClick={() => window.location.href = '/'}
        className={cn(
          "mt-8 px-6 py-3 text-lg font-semibold text-gray-900",
          "bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400",
          "rounded-lg shadow-lg transition-transform transform hover:scale-105 hover:-translate-y-1",
          "hover:shadow-2xl focus:outline-none",
          "focus:ring-2 focus:ring-indigo-400 focus:ring-opacity-50"
        )}
      >
        Go to Homepage
      </Button>
    </div>
  );
};