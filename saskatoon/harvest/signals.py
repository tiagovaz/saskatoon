from crequest.middleware import CrequestMiddleware
from django.core.mail import send_mail


def _send_mail(subject, message, mail_to):
    subject = '[Sakatoon] ' + subject
    send_mail(
            subject,
            message,
            'info@lesfruitsdefendus.org', #FIXME: add in settings
            mail_to,
            fail_silently=False,
        )

def changed_by(sender, instance, **kwargs):
    current_request = CrequestMiddleware.get_request()
    if current_request:
        instance.changed_by = current_request.user
    else:
        instance.changed_by = None

def comment_send_mail(sender, instance, **kwargs):
    current_request = CrequestMiddleware.get_request()

    # Send email only if comment comes from someone else
    if instance.author.email != instance.harvest.pick_leader.email:
        # Building email content
        pick_leader_email = []
        pick_leader_email.append(instance.harvest.pick_leader.email)
        pick_leader_name  = instance.harvest.pick_leader.person.first_name
        mail_subject = u"New comment from %s" % instance.author
        message = u'Hi %s, \n\n\
On %s %s left the following comment\n\
in the harvest "%s":\n\n\
%s\n\n\
You can see all comments related to this harvest at\n\
http://saskatoon.lesfruitsdefendus.org/harvest/%s.\n\n\
Yours,\n\
--\n\
Saskatoon Harvest System' % (pick_leader_name, instance.created_date.strftime('%b %d at %H:%M'), instance.author, instance.harvest.property.publishable_location, instance.content, instance.harvest.id)

        # Sending email to pick leader
        _send_mail(mail_subject, message, pick_leader_email)
