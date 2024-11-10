[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/fULRwKMW)


# KURLY - URL SHORTENER

## ⭐ Features ⭐

- Shortening url locally/remotly
- Password protect, expire date, limit url uses, etc.
- Custom ShortCodes
- Customizable preferences


## 🚀 Tech Stack 🚀

 * Python
 * Flask
 * Qt
 * JavaScript
 * SQLite


## 📥 Installation 📥

Tested and maintained on Python **[1.13.0](https://www.python.org/downloads/release/python-3130/)**

### 🧱 Install Dependencies

Install dependencies with **pip**

```bash
pip install -r requirements.txt
```

### ⚒️ Make a Build

 - **Build using pre-made batch file**

This is the project's root directory. Find a file named `BUILD.BAT` and open it.

If you encounter any issues, feel free to contact us.

 - **Build using CLI**

```bash
pip install -r requirements.txt
pip install pyinstaller
pyinstaller main.spec
```
When this build is complete you will find the application in the `dist` folder.
    
## 📎 Usage 📎

### 🔗 Create a Short URL

Paste your long URL in the field `Long URL`.

Then click `Add URL` to create it.

### ⚙️ Adding advanced features to your URL *(Optional)*

Before you click `Add URL`, you can add more features to the short URL, such as a password, expiration date, etc.

Check the `Advanced URL Settings` to open the URL Settings.

#### ✏️ Custom Short Code

To add a custom short code, check the `Custom Short URL` box and edit the `Short URL` field.

#### 🔒 Password protect your URL

Check the `Password` box and type a password to protect your URL.

#### 🔩  Limit the URL uses

Check the `Set max uses` box and enter a value.

#### ⌛ Expire Date

Set an expiration date by checking the `Expire Date` box.

### 📝 Updating existing URL

You can update an existing one by clicking on it in the URL table or typing the short code of the url in the `Check URL` field at the bottom of the window. Change the fields to the new information and click `Update URL`.

### ⚙️ Settings

Open the settings dialogue by clicking `File` in the top-left of the window and then `Settings` or press `Ctrl + P`

#### 📃 General Tab

- `Short URL Length` is the length of the auto generated short code.

- `Max Short URL Length` is the maximum length of the short code that the user can enter.

- `Rename passwd protected URLs in table` if checked will hide the URLs in the URL table.

- `Show hidden URL` if check will show all hidden URL in the table.

> (*) **Hidden URL** is a expired or maxed URL.

#### 🎨 Appearance Tab

- If you encounter any graphic issues, check the `Use Default Theme` setting.

#### 🧾 Database Tab

- `DB Name` This is the database name, whether local or remote.

- `Remote DB` when its checked will show openings for a remote database.

- `Host Name` and `Host Port` enter your remote database details to connect to the remote database.

#### 📶 Router Server

- Check `Debug` to enable flask debug server.

- `Router Port` is the local port for routing. `e.g., localhost:5000, 127.0.0.1:27017`




