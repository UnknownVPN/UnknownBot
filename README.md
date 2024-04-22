<p align="center">
<img src="images/bot.jpg" class="center">
</p>

# [UnknownBot](https://t.me/Unknownvpnbot)
Public sponsorship source for UnknownVpn sales bot

### Who is UknownVpn?

UnknownVpn provides high-speed VPN configurations powered by the V2ray protocol. We focus on ease of use and deliver configs directly [in Telegram](https://t.me/Unknownvpnbot).

### Features
- ⚡️ Fast connections - Our network is optimized for speed with minimal latency and jitter.
- 🔐 Strong encryption - All connections are secured with industry standard encryption.
- 🏁 Multi-location servers - Choose from servers located around the world.
- ♨️ V2ray protocol - Flexible and powerful protocol.
- 🤖 No activity logs - We do not track or store any logs of your online activities.
- 💭 24/7 Support - Our friendly support team is available around the clock, 365 days a year.
- 🕕 24 Hour Resolution Guarantee - We understand connectivity issues disrupt your work and activities.

## [Installation](https://t.me/Unknownvpnbot)

#### Requirements

- Python 3.8 or later
- MongoDB

#### Steps

1. Clone the repository
   ```bash
   git clone https://github.com/UnknownVPN/UnknownBot.git
   ```
2. Install Python packages
   ```bash
   pip install -r requirements.txt
   ```
3. Install and run [MongoDB](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/)

   ```bash
   # Install MongoDB
   sudo apt install mongodb

   # Start MongoDB
   sudo service mongodb start
   ```
4. Configure settings
   - Put you configguration in `config.ini`.

5. Run the bot
   ```bash
   python3 main.py
   ```