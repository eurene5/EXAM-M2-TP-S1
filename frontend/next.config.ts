import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Requis pour le build Docker multi-stage (stage "runner" minimal)
  output: "standalone",
};

export default nextConfig;
