**Meet "CS50!" – Your CS Buddy for Harvard's Computer Science Adventure**

**Get ready to rock your coding world with CS50! This Chrome extension is your shortcut to all the cool stuff happening in Harvard's CS50 course.**

**Keep updated on the latest CS50 news!**
**Ver 1.1 is out, now featuring David Malan screaming CS50 in each notification!**

**🎨 Easy Peasy Interface:**
CS50! keeps it simple and snazzy. One click, and you're hooked up to the newest CS50 content. No fuss, all fun.

**🚀 Instant Updates:**
Don't miss a beat! CS50! shoots you a quick heads-up whenever a fresh CS50 YouTube video drops. Stay on top of the latest lectures and coding magic.

**👌Keep on keeping on!**
Most users start their CS50 adventure but never finish it! With this new tool, keeping hooked has never been easier!

#### Video Demo:  <URL 'https://www.youtube.com/watch?v=-VE_QAPtXuU'>

## DISCLAIMERS =
* The CS50! Chrome extension does not claim ownership of any videos featured; all content belongs to the CS50 YouTube channel.
* Update Notice: Version 1.0 has been patched, resolving notification bugs for a smoother user experience.
* Acknowledgment: Special thanks to David J. Malan for delivering an exceptional course.
* Future Updates: We commit to making necessary updates to enhance your experience. Stay tuned for more improvements.

## How To Make Your Own CS50 Extension!

* 1. Create Your Project Folder:
Start by creating a folder for your Chrome extension project. Give it a meaningful name, such as "CS50_Extension."

* 2. Create Manifest File:
Inside your project folder, create a file named manifest.json. This file is crucial for defining your extension's properties.
---------------------------------------------------------------------------
 manifest.json
{
  "manifest_version": 2,
  "name": "CS50!",
  "version": "1.0",
  "description": "Stay updated with the latest CS50 videos.",
  "permissions": ["storage", "notifications"],
  "browser_action": {
    "default_icon": "icon.png",
    "default_popup": "popup.html"
  },
  "icons": {
    "16": "icon.png",
    "48": "icon.png",
    "128": "icon.png"
  }
}
---------------------------------------------------------------------------
* 3. Create Popup HTML File:
Create an HTML file for the popup. Name it popup.html
---------------------------------------------------------------------------
 !DOCTYPE html>
 html>
 head>
  title>CS50! Extension</title
/head>
body>
  h1>Welcome to CS50!</h1
/body>
/html>
---------------------------------------------------------------------------
* 4. Create Extension Icon:
Design an icon for your extension and save it as icon.png in your project folder.

* 5. Load the Extension:
Open Chrome and navigate to chrome://extensions/.

* 6. Enable Developer Mode:
Toggle on "Developer mode" at the top right.

* 7. Load Unpacked Extension:
Click on "Load unpacked" and select your project folder.

* 8. Test Your Extension:
You should see your extension icon in the Chrome toolbar. Click it to test the popup.

* 9. Update Your Extension:
As you make changes, update the version number in manifest.json, and reload your extension in the Chrome extensions page.

* 10. Distribution (Optional):
If you plan to distribute your extension, consider publishing it on the Chrome Web Store.

## Additional notes: ##

* Permissions: Adjust the permissions in manifest.json based on the features your extension requires.
* Customization: Customize HTML, CSS, and JavaScript in popup.html to suit your extension's functionality.
