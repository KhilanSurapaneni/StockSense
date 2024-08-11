import React from "react";
import { DashboardButton } from "@/components/Landing/DashboardButton";
import { Separator } from "@/components/ui/separator";
import { Title } from "@/components/Landing/Title";
import { Description } from "@/components/Landing/Description";

export const Landing: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 p-8">
      <Title />
      <Description />
      <Separator className="my-8 w-3/4 bg-gray-700" />
      <DashboardButton />
    </div>
  );
};
