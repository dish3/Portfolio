/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ["@nova/types", "@nova/config"],
  reactStrictMode: true,
};

export default nextConfig;
