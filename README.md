# Stremio Community Subtitles Addon

A Stremio addon that enables you to use custom subtitles on any device - something normally only possible on desktop Stremio. Simply upload your subtitle files for the video you just started watching, and they'll be instantly available across all your devices through the addon.

Every subtitle you upload helps build a community database that benefits all users. The OpenSubtitles integration allows manual selection of any available subtitles and linking them to specific video versions, ensuring perfectly synchronized subtitles for future viewers.

## ✨ Features

- **📱 Cross-Device Subtitle Support** - Use custom subtitles on any device (mobile, TV, desktop)
- **🌍 Community Database Building** - Every uploaded subtitle contributes to a shared database helping all users
- **🎯 Manual OpenSubtitles Selection** - Choose any subtitle from OpenSubtitles and link it to specific video versions
- **🔗 Perfect Synchronization** - Linked subtitles ensure future viewers get perfectly timed subtitles for the same video file
- **⚡ Instant Upload & Access** - Upload subtitles for videos you're currently watching and access them immediately
- **Subtitle Voting System** - Community-driven quality control through upvoting/downvoting

## 🚀 Installation

To install the addon:

1. Visit [The Addon Website](https://stremio-community-subtitles.top) 
2. Create account
3. Confirm email
4. Login
5. From the [configuration page](https://stremio-community-subtitles.top/configure) copy your personal manifest URL
6. Open Stremio and go to the addon search box
7. Paste the copied manifest URL into the addon search box and press Enter. Alternatively, you can click "Install In Stremio" to automatically add the addon to Stremio
8. In Stremio, click install, and the addon will be added and ready for use

## 🔧 OpenSubtitles.com Integration

To enable OpenSubtitles integration for access to a broader subtitle database:

### Step 1: Create OpenSubtitles API Consumer
1. Register and login at [OpenSubtitles.com](https://www.opensubtitles.com/)
2. Go to your account menu and select **"API Consumer"** - [https://www.opensubtitles.com/en/consumers](https://www.opensubtitles.com/en/consumers)
3. Click **"NEW CONSUMER"** button
4. Enter any name for your consumer
5. **Uncheck** "Allow anonymous downloads"
6. Click **"SAVE"**
7. Copy your generated API key

### Step 2: Configure Integration
1. Login to your [addon account settings](https://stremio-community-subtitles.top/account)
2. Check **"Use OpenSubtitles Integration"**
3. Enter your OpenSubtitles username, password, and API key
4. Save your settings

Once configured, you can manually select any OpenSubtitles subtitle for your videos, and link them to specific video files so other users get perfectly synchronized subtitles.

### Why API Key is Required
The personal API key bypasses OpenSubtitles' free API limitations (5 requests per second per IP). With your own API key, you get dedicated rate limits and improved subtitle search performance. See [OpenSubtitles API pricing](https://opensubtitles.stoplight.io/docs/opensubtitles-api/f65bc8dd4aef7-api-subscription-prices) for more details.

## 📱 Usage

### Quick Start for Any Device:
1. **Start Watching** - Begin playing any movie or TV show on any device (mobile, TV, desktop)
2. **Check Homepage** - Visit the [addon homepage](https://stremio-community-subtitles.top) to see your recent viewing history
3. **Upload or Select Subtitles** - Click on the video you're watching and either:
   - Upload your own subtitle file, or
   - Browse and select from OpenSubtitles database
4. **Link to Video** - The subtitle gets linked to your specific video file
5. **Instant Access** - Return to Stremio and select the Community Subtitles available in the subtitles list
6. **Help Others** - Your contribution is now available for other users watching the same video file

## 🎯 How It Works

**The Key Innovation:** Stremio's desktop app allows loading external subtitle files by drag and drop, but mobile and TV apps don't support this feature. This addon bridges that gap by letting you upload or select subtitles through the web interface and instantly access them on any device.

**Community Building:** Every subtitle uploaded or linked helps create a comprehensive database. When you link an OpenSubtitles entry to a specific video file, future users watching the same file automatically get perfectly synchronized subtitles.

The addon intelligently matches subtitles using:
- **Video Hash Matching** - Precise synchronization with your specific video files
- **Community Contributions** - Benefit from subtitles uploaded and linked by other users
- **OpenSubtitles Integration** - Manual selection and linking of any available subtitles
- **Viewing History Tracking** - Your recent activity appears on the homepage for easy management
- **Quality Voting** - Community-driven rating system for subtitle quality

## 🤝 Support

If you want to thank me for the addon, you can [buy me a coffee](https://buycoffee.to/skoruppa) ☕

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Website:** [stremio-community-subtitles.top](https://stremio-community-subtitles.top)