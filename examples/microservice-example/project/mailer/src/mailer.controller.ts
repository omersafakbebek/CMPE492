import { Controller, HttpStatus } from '@nestjs/common';
import { MessagePattern } from '@nestjs/microservices';
import { MailerService } from '@nestjs-modules/mailer';

import { ConfigService } from './services/config/config.service';
import { IEmailData } from './interfaces/email-data.interface';
import { IMailSendResponse } from './interfaces/mail-send-response.interface';

@Controller()
export class MailerController {
  constructor(
    private readonly mailerService: MailerService,
    private readonly configService: ConfigService,
  ) {}

  @MessagePattern('mail_send')
  async mailSend(data: IEmailData): Promise<IMailSendResponse> {
    // if (!this.configService.get('emailsDisabled')) {
      await this.mailerService.sendMail(data);
    // }
    return {
      status: HttpStatus.ACCEPTED,
      message: 'mail_send_success',
    };
  }
}
