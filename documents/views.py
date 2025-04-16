from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import View

from .models import Document
from .tasks import process_document


class DocumentsView(View):
    def get(self, request):
        return render(request, "documents/index.html")

    def post(self, request):
        try:
            file = request.FILES.get("file")
            if not file:
                messages.error(request, "No file selected")
                return redirect("documents")

            document = Document.objects.create(file=file, name=file.name)

            process_document(document)
        except UnicodeEncodeError:
            messages.error(request, "File name must be in ASCII characters only")
        except Exception as e:
            messages.error(request, "An error occurred while uploading the file.")

        return redirect("documents")
