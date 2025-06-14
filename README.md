# TCP Port Scanner

<p align="center">
    <img width="700"
        src="images/002.png"
        alt="Banner"
        style="float: left; margin-right: 10px;">
</p>

**TCP Port Scanner** is a fast tool to scan open ports. You can use it giving the **target host** and **port**.

<p align="center">
    <img width="500"
        src="images/001.png"
        alt="Scanning example"
        style="float: left; margin-right: 10px;">
</p>

## How can I use it?

- **Target:**
    First, you need to give a target using **-t / --target** argument.<br/>
    Example: -t 192.168.0.1

- **Port:**
    Second, you need to give a specific, range or list of ports using **-p / --port** argument.<br/>
    Examples:

    - -p 80
    - -p 22,80,443,8080
    - -p 1-600 (Scan from 1 to 600)
