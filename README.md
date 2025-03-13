  <h3 align="center">PH-DL</h3>

  <p align="center">
    The PornHub Downloader is a powerfull script used to download and manage both videos and pictures
  </p>

<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>

## About The Project
<img src="assets/screenshot1.png" alt="Image of product">

The script will allow you to download both images and also files  
If you don't know what I'm talking about when I say images you can locate them [here (NSFW)](https://www.pornhub.com/albums)  

The script supports what I call categories, when you download a video the script will prompt you to type out a category where it will put the downloaded file there, see the image below

<img src="assets/screenshot2.png" alt="Image of product 2">

The script takes the full url when downloading the files, that looks like this:  
`https://www.pornhub.com/view_video.php?viewkey=ph600dfff994b80`

### Built With

*On inital launch the script will automatically prompt you to install them*
* [Requests](https://github.com/psf/requests)
* [Youtube-Dl](https://github.com/ytdl-org/youtube-dl)
* [BS4](https://www.crummy.com/software/BeautifulSoup/)
* [pynotifier](https://github.com/YuriyLisovskiy/pynotifier)

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites
You need to install Python, that can be done [here](https://www.python.org)

### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/logicguy1/Discord-Nitro-Generator-and-Checker.git
   ```

2. Run the files
   ```sh
   python main.py
   ```

From there simply say yes to everything the script asks you for (after reading and agreeing of course) and you're set

## Usage
After <a href="#installation">running the files</a> everything should be set-up and ready to go for you, if you want to download a video, press `1` and insert the URL, it will download the files, give you a notification and then you can choose where you want the video to be saved (what category)

Downloading pictures and albums is a little different since you can either use a single image or a whole album

Album urls: https://www.pornhub.com/album/70564671  
Picture urls: https://www.pornhub.com/photo/803965741  

They get downloaded at the same place in the script
