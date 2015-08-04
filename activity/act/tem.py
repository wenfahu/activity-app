
    '''
    thumbnail = models.ImageField(
	upload_to=thumbnail_folder,
	max_length=500,
	null=True,
	blank=True
    )
    def create_thumbnail(self):
        if not self.avatar:
            return
        from PIL import Image
        from io import StringIO, BytesIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        THUMBNAIL_SIZE = (200, 200)

        DJANGO_TYPE = self.avatar.file.content_type

        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpg'
            FILE_EXTENSITION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSITION = 'png'

        avatar = Image.open(BytesIO(self.avatar.read()))
        avatar.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        tmp_handle = BytesIO()
        avatar.save(tmp_handle, PIL_TYPE)
        tmp_handle.seek(0)
        suf = SimpleUploadedFile(os.path.split(self.avatar.name)[-1],
                                 tmp_handle.read(), content_type=DJANGO_TYPE)
        self.avatar.save(
            '%s_thumbnail.%s' %
            (os.path.splitext(
                suf.name)[0],
                'png'),
            suf,
            save=False)

    def save(self):
        self.create_thumbnail()

        super(UserProfile, self).save()
    '''
