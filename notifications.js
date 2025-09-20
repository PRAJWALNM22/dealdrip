const TelegramBot = require('node-telegram-bot-api');
const nodemailer = require('nodemailer');
require('dotenv').config();

class NotificationService {
    constructor() {
        // Telegram Bot Configuration
        this.telegramBot = null;
        this.telegramChatId = process.env.TELEGRAM_CHAT_ID;
        
        if (process.env.TELEGRAM_BOT_TOKEN) {
            this.telegramBot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN, {polling: false});
        }

        // Email Configuration (Gmail SMTP)
        this.emailTransporter = nodemailer.createTransport({
            service: 'gmail',
            auth: {
                user: process.env.EMAIL_USER,
                pass: process.env.EMAIL_APP_PASSWORD // Gmail App Password
            }
        });
    }

    // Send Telegram Notification
    async sendTelegramMessage(message) {
        if (!this.telegramBot || !this.telegramChatId) {
            console.log('❌ Telegram not configured');
            return false;
        }

        try {
            await this.telegramBot.sendMessage(this.telegramChatId, message);
            console.log('✅ Telegram message sent successfully');
            return true;
        } catch (error) {
            console.error('❌ Telegram error:', error.message);
            return false;
        }
    }

    // Send Email Notification
    async sendEmailNotification(subject, message, toEmail) {
        if (!process.env.EMAIL_USER) {
            console.log('❌ Email not configured');
            return false;
        }

        const mailOptions = {
            from: process.env.EMAIL_USER,
            to: toEmail || process.env.DEFAULT_EMAIL_RECIPIENT,
            subject: subject,
            html: `
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center;">
                        <h1 style="color: white; margin: 0;">🔥 DealDrip Alert</h1>
                    </div>
                    <div style="padding: 20px; background: #f9f9f9;">
                        <h2 style="color: #333;">${subject}</h2>
                        <div style="background: white; padding: 15px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                            ${message.replace(/\n/g, '<br>')}
                        </div>
                        <p style="text-align: center; color: #666; margin-top: 20px;">
                            <em>Sent by DealDrip Notification System</em>
                        </p>
                    </div>
                </div>
            `
        };

        try {
            await this.emailTransporter.sendMail(mailOptions);
            console.log('✅ Email sent successfully');
            return true;
        } catch (error) {
            console.error('❌ Email error:', error.message);
            return false;
        }
    }

    // Send Both Notifications
    async sendNotification(title, message, emailRecipient = null) {
        console.log(`📢 Sending notification: ${title}`);
        
        const telegramMessage = `🔥 *${title}*\n\n${message}`;
        
        const results = await Promise.allSettled([
            this.sendTelegramMessage(telegramMessage),
            this.sendEmailNotification(title, message, emailRecipient)
        ]);

        const telegramSuccess = results[0].status === 'fulfilled' && results[0].value;
        const emailSuccess = results[1].status === 'fulfilled' && results[1].value;

        console.log(`📊 Results: Telegram: ${telegramSuccess ? '✅' : '❌'} | Email: ${emailSuccess ? '✅' : '❌'}`);
        
        return {
            telegram: telegramSuccess,
            email: emailSuccess,
            success: telegramSuccess || emailSuccess
        };
    }

    // Test Notifications
    async testNotifications() {
        console.log('🧪 Testing notification system...\n');
        
        const testMessage = `This is a test notification from DealDrip!\n\nTimestamp: ${new Date().toLocaleString()}`;
        
        return await this.sendNotification('Test Notification', testMessage);
    }
}

// Example usage
async function main() {
    const notifier = new NotificationService();
    
    // Test the notification system
    await notifier.testNotifications();
    
    // Example deal notification
    // await notifier.sendNotification(
    //     'New Deal Alert!',
    //     'MacBook Pro 16" - 50% OFF\nOriginal Price: $2,499\nSale Price: $1,249\nSavings: $1,250\n\nLink: https://example.com/deal'
    // );
}

// Export for use in other files
module.exports = NotificationService;

// Run if called directly
if (require.main === module) {
    main().catch(console.error);
}