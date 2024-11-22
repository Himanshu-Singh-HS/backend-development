from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Flowable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

class BoxWithLines(Flowable):
    """A custom Flowable for creating a box with four horizontal lines."""
    def __init__(self, width, height, title, content, styles):
        super().__init__()
        self.width = width
        self.height = height
        self.title = title
        self.content = content
        self.styles = styles

    def draw(self):
        # Draw the outer box
        self.canv.rect(0, 0, self.width, self.height, stroke=1, fill=0)
        
        # Draw the horizontal lines inside the box
        line_spacing = self.height / 5
        for i in range(1, 5):
            y = i * line_spacing
            self.canv.line(0, y, self.width, y)

        # Add the title and content
        self.canv.setFont("Helvetica-Bold", 10)
        self.canv.drawString(10, self.height - 15, self.title)
        self.canv.setFont("Helvetica", 9)
        text_y = self.height - 30
        for line in self.content.split("\n"):
            self.canv.drawString(10, text_y, line)
            text_y -= 12

def create_pdf_with_boxes(file_path):
    # Create the document template
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Define box dimensions
    page_width, page_height = letter
    margin = 50
    box_width = page_width - 2 * margin
    box_height = (page_height - 2 * margin) / 4

    # Content for each box
    box_texts = [
        ("Title Box 1", "This is the content for box 1.\nIt can have multiple lines."),
        ("Title Box 2", "This is the content for box 2.\nAdd more details as needed."),
        ("Title Box 3", "Content for box 3 goes here.\nMake it descriptive."),
        ("Title Box 4", "Final box content.\nSummarize or conclude."),
    ]

    # Create each box with lines and content
    for title, content in box_texts:
        box = BoxWithLines(box_width, box_height, title, content, styles)
        elements.append(box)
        elements.append(Spacer(1, 12))  # Add some spacing between boxes

    # Build the PDF
    doc.build(elements)

# Generate the PDF
create_pdf_with_boxes("boxes_with_lines_and_content.pdf")


