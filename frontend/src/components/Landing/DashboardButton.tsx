import React from "react";
import { Button } from "@/components/ui/button";

export const DashboardButton: React.FC = () => {
  return (
    <Button className="relative group px-8 py-4 text-xl font-medium text-gray-900 bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 rounded-lg shadow-lg transition-transform transform hover:scale-105 hover:-translate-y-1 hover:shadow-2xl focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-opacity-50">
      <span className="relative z-10">View Dashboard</span>
      <span className="absolute inset-0 rounded-lg bg-gradient-to-r from-purple-500 to-pink-500 opacity-0 transition-opacity duration-300 group-hover:opacity-100"></span>
    </Button>
  );
};