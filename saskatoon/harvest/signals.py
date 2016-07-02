from crequest.middleware import CrequestMiddleware


def changed_by(sender, instance, **kwargs):
    current_request = CrequestMiddleware.get_request()
    if current_request:
        print 'tititititititititti'
        instance.changed_by = current_request.user
    else:
        instance.changed_by = 'Unknown'

    print 'tototototototototototototototototo'
    print current_request.user