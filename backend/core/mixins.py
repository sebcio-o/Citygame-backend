class ListDetailSerializerSplitMixin:
    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        return self.detail_serializer_class
