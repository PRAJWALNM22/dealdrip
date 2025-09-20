// Simple notification sender for Python to call
const NotificationService = require('./notifications');

async function main() {
    const args = process.argv.slice(2);
    
    if (args.length < 3) {
        console.log('Usage: node send_notification.js "title" "message" "product_url"');
        process.exit(1);
    }
    
    const [title, message, productUrl] = args;
    
    const notifier = new NotificationService();
    
    try {
        const result = await notifier.sendNotification(title, message);
        
        if (result.success) {
            console.log('✅ NOTIFICATION_SUCCESS');
            console.log(`Telegram: ${result.telegram ? '✅' : '❌'}`);
            console.log(`Email: ${result.email ? '✅' : '❌'}`);
        } else {
            console.log('❌ NOTIFICATION_FAILED');
        }
    } catch (error) {
        console.log('❌ NOTIFICATION_ERROR:', error.message);
    }
}

main();