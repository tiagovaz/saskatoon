# coding: utf-8

from member.models import Notification


def get_number_notification(request):
    """
    Return the number of notification for the current user
    :param request: the current request HTTP
    :return: number of notification of current user
    """

    if request.user.is_authenticated():
        notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        )

        number_of_notification = notifications.count()
    
        for notification in notifications:
            print(request.build_absolute_uri())
            if notification.url == request.build_absolute_uri():
                notification.is_read = True
                notification.save()
                number_of_notification -= 1
    
    else:
        number_of_notification = 0
    return {
            "number_of_notification": number_of_notification
    }
