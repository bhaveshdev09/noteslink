from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from notes.models import Note
from notes.serializers import NoteSerializer, ShareNoteSerializer
from notes import permissions as custompermissions


class CreateNoteView(generics.CreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        serializer.context.update({"request": self.request})
        return serializer


class RetriveUpdateNoteView(generics.RetrieveUpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [custompermissions.IsOwnerOrSharedUser]


class ShareNoteView(generics.CreateAPIView):
    queryset = Note.objects.all()
    serializer_class = ShareNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            serializer.update(
                instance=data.get("note"),
                validated_data=serializer.validated_data,
                auth_user=self.request.user,
            )
            context = {"msg": "note shared successfully"}
            return Response(context, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
