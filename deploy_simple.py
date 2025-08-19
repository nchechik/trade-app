#!/usr/bin/env python3
"""
Simple Deployment Script
Makes your Forex dashboard accessible from anywhere on your network.
"""

import http.server
import socketserver
import socket
import webbrowser
import os
from pathlib import Path

def get_local_ip():
    """Get the local IP address for network access."""
    try:
        # Get local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "localhost"

def create_deployment_files():
    """Create deployment-ready files."""
    print("📁 Creating deployment files...")
    
    # Create deployment directory
    deploy_dir = Path("deploy")
    deploy_dir.mkdir(exist_ok=True)
    
    # Copy dashboard
    dashboard_source = Path("static_dashboard.html")
    dashboard_dest = deploy_dir / "index.html"
    
    if dashboard_source.exists():
        with open(dashboard_source, 'r') as src:
            content = src.read()
        
        with open(dashboard_dest, 'w') as dest:
            dest.write(content)
        
        print("✅ Dashboard copied to deploy/index.html")
    else:
        print("❌ Dashboard file not found")
        return False
    
    # Create README for deployment
    readme_content = """# 🚀 Forex Trading Dashboard - Ready to Deploy!

## 📁 Files:
- `index.html` - Your dashboard (rename from static_dashboard.html)

## 🌐 Deploy to Any Platform:

### 🐙 GitHub Pages:
1. Create new repository
2. Upload index.html
3. Enable Pages in Settings

### 🚀 Netlify:
1. Go to netlify.com
2. Drag & drop index.html
3. Get live URL instantly

### ⚡ Vercel:
1. Go to vercel.com
2. Import from GitHub
3. Deploy automatically

## 📱 Access from Anywhere:
- Works on all devices
- Mobile-optimized
- Auto-refreshing data
- No installation required

## 🎯 Features:
- Live Forex trading simulation
- Real-time balance updates
- Professional dashboard design
- Mobile-friendly interface
"""
    
    with open(deploy_dir / "README.md", 'w') as f:
        f.write(readme_content)
    
    print("✅ README.md created")
    return True

def start_server(port=8080):
    """Start HTTP server to serve the dashboard."""
    local_ip = get_local_ip()
    
    # Change to deployment directory
    os.chdir("deploy")
    
    # Create server
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print("🚀 Forex Trading Dashboard Deployed!")
        print("=" * 60)
        print(f"📱 Local Access: http://localhost:{port}")
        print(f"🌐 Network Access: http://{local_ip}:{port}")
        print("=" * 60)
        print("💡 To access from your phone:")
        print(f"   1. Make sure phone is on same WiFi network")
        print(f"   2. Open browser and go to: http://{local_ip}:{port}")
        print("=" * 60)
        print("🎯 Dashboard Features:")
        print("   ✅ Live demo data generation")
        print("   ✅ Auto-refresh every 30 seconds")
        print("   ✅ Mobile-optimized design")
        print("   ✅ Professional interface")
        print("=" * 60)
        print("🌍 To deploy to internet:")
        print("   1. Upload deploy/index.html to any hosting service")
        print("   2. Rename to index.html")
        print("   3. Get live URL instantly!")
        print("=" * 60)
        print("💡 Press Ctrl+C to stop server")
        
        try:
            # Open in default browser
            webbrowser.open(f"http://localhost:{port}")
            print("🌐 Opened dashboard in your browser!")
            
            # Start server
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
        finally:
            httpd.server_close()

def main():
    """Main deployment function."""
    print("🚀 Forex Trading Dashboard Deployment")
    print("=" * 60)
    
    # Create deployment files
    if not create_deployment_files():
        print("❌ Failed to create deployment files")
        return
    
    print("\n🎯 Starting local server...")
    print("=" * 60)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()