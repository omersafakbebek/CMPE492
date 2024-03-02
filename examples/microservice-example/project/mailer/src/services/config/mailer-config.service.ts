import { MailerOptionsFactory, MailerOptions } from '@nestjs-modules/mailer';

export class MailerConfigService implements MailerOptionsFactory {
  createMailerOptions(): MailerOptions {
    return {
      transport: {
        host: "smtp.gmail.com",
        secure: false,
        auth: {
          user: process.env.MAILER_FROM,
          pass: process.env.MAILER_PASSWORD
        }
      },
      defaults: {
        from: process.env.MAILER_FROM,
      },
    };
  }
}
