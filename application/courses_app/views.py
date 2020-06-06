from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics

from .models import StudentStream, StudentGroup, GroupInStream, Course, Lesson, StudentLessonResult, \
    ClassmatesCheckedTask, TaskOption, StudentResult, Check
from .serializers import StudentStreamSerializer, StudentGroupSerializer, \
    StudentGroupSerializer, GroupMemberSerializer, CourseSerializer, \
    LessonSerializer, StudentLessonResultSerializer, \
    CreateStudentLessonResultSerializer, ClassmatesCheckedTaskSerializer, \
    TaskOptionSerializer, StudentResultSerializer, CheckSerializer
from .utils import get_object_or_none


class StudentStreamListCreateView(generics.ListCreateAPIView):
    queryset = StudentStream.objects.all()
    serializer_class = StudentStreamSerializer
    permission_classes = [permissions.AllowAny]


class StudentStreamRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = StudentStream.objects.all()
    serializer_class = StudentStreamSerializer
    permission_classes = [permissions.AllowAny]


class GroupInStreamListCreateView(generics.ListCreateAPIView):
    queryset = StudentStream.objects.all()
    serializer_class = StudentGroupSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        stream = get_object_or_none(StudentStream, {'id': pk})

        if stream is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(stream.groups, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        stream = get_object_or_none(StudentStream, {'id': pk})

        if stream is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if 'group_id' not in request.data:
            return Response({'group_id': ['Отсутствует обязательное поле group_id']},
                            status=status.HTTP_400_BAD_REQUEST)

        group = get_object_or_none(StudentGroup, {'id': request.data['group_id']})

        if group is None:
            return Response({'group_id': ['Группа с указанным group_id не была найдена']},
                            status=status.HTTP_404_NOT_FOUND)

        group_in_stream = GroupInStream(group=group, stream=stream)
        group_in_stream.save()

        serializer = self.serializer_class(stream.groups, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentGroupListCreateView(generics.ListCreateAPIView):
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer
    permission_classes = [permissions.AllowAny]


class StudentGroupRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer
    permission_classes = [permissions.AllowAny]


class StudentGroupMembersListCreateView(generics.ListCreateAPIView):
    queryset = StudentGroup.objects.all()
    serializer_class = GroupMemberSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        student_group = self.queryset.get(id=pk)
        members = student_group.members.all()
        serializer = self.serializer_class(members, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        student_group = self.queryset.get(id=pk)

        if 'user_id' not in request.data:
            return Response({'user_id': ['Отсутствует обязательное поле user_id']},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            student_group.add_member(request.data['user_id'])
        except ObjectDoesNotExist:
            return Response({'user_id': ['Пользователь с указанным user_id не был найден']},
                            status=status.HTTP_404_NOT_FOUND)

        members = student_group.members.all()
        serializer = self.serializer_class(members, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class StudentLessonResultCreateView(generics.CreateAPIView):
    queryset = StudentLessonResult.objects.all()
    serializer_class = CreateStudentLessonResultSerializer


class StudentLessonResultRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = StudentLessonResult.objects.all()
    serializer_class = StudentLessonResultSerializer


class StudentLessonResultListView(generics.ListAPIView):
    queryset = StudentLessonResult.objects.all()
    serializer_class = StudentLessonResultSerializer


class ClassmatesCheckedTaskListCreateView(generics.ListCreateAPIView):
    queryset = ClassmatesCheckedTask.objects.all()
    serializer_class = ClassmatesCheckedTaskSerializer
    permission_classes = [permissions.AllowAny]


class ClassmatesCheckedTaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassmatesCheckedTask.objects.all()
    serializer_class = ClassmatesCheckedTaskSerializer
    permission_classes = [permissions.AllowAny]


class TaskOptionListCreateView(generics.ListCreateAPIView):
    queryset = TaskOption.objects.all()
    serializer_class = TaskOptionSerializer
    permission_classes = [permissions.AllowAny]


class TaskOptionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskOption.objects.all()
    serializer_class = TaskOptionSerializer
    permission_classes = [permissions.AllowAny]


class StudentResultListCreateView(generics.ListCreateAPIView):
    queryset = StudentResult.objects.all()
    serializer_class = StudentResultSerializer


class StudentResultRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentResult.objects.all()
    serializer_class = StudentResultSerializer
    permission_classes = [permissions.AllowAny]


class CheckListCreateView(generics.ListCreateAPIView):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer
    permission_classes = [permissions.AllowAny]


class CheckRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer
    permission_classes = [permissions.AllowAny]
