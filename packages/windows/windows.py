from os import path

from PySide6.QtCore import Signal

from packages.ui.DesignUI import MainWidget, Label, SpinBox, LineEdit, ListWidget, PushButton, \
    VBoxLayout, HBoxLayout, Shortcut, KeySequence, ListWidgetItem, Icon, MessageBoxWarning, MessageBoxCritical, \
    Thread, Object, ProgressDialog

from packages.api.image import CustomImage


class Image_worker(Object):
    # customs signals
    converted = Signal(object, bool)  # We can send parameter to signal, give type of variable as argument
    finished = Signal()

    def __init__(self, images_to_convert, output_folder, size, quality):
        super().__init__()
        self.images_to_convert = images_to_convert
        self.output_folder = output_folder
        self.size = size
        self.quality = quality
        self.run = True

    def convert(self):
        for image_item in self.images_to_convert:
            if self.run:
                image = CustomImage(image_item.text(), self.output_folder)
                status = image.compress(self.size, self.quality)
                self.converted.emit(image_item, status)  # run signal
        self.finished.emit()  # run signal when function convert() finished


class Windows(MainWidget):
    def __init__(self):
        super().__init__("Image Compressor", 350, 500)
        self.setAcceptDrops(True)  # To accept drop action

        # Attributes
        self.thread = Thread()
        self.size_label = Label("Size ratio (%)")
        self.quality_label = Label("Quality (%)")
        self.output_folder_label = Label("Output Folder")
        self.size_spinbox = SpinBox()
        self.quality_spinbox = SpinBox()
        self.output_folder_lineedit = LineEdit("Name of output folder...")
        self.list_images = ListWidget()
        self.drop_label = Label("^ Drop images to compress ^")
        self.compress_button = PushButton("Compress")

        # Custom widget
        self.size_spinbox.setRange(1, 100)
        self.size_spinbox.setValue(50)

        self.quality_spinbox.setRange(1, 100)
        self.quality_spinbox.setValue(75)

        self.drop_label.setVisible(False)

        # Icons
        self.correct_icon = Icon(path.join('resources', 'icons', 'correct.png'))
        self.warning_icon = Icon(path.join('resources', 'icons', 'warning.png'))

        # Layout
        label_v_layout = VBoxLayout()
        label_v_layout.addWidget(self.size_label)
        label_v_layout.addWidget(self.quality_label)
        label_v_layout.addWidget(self.output_folder_label)

        spinbox_v_layout = VBoxLayout()
        spinbox_v_layout.addWidget(self.size_spinbox)
        spinbox_v_layout.addWidget(self.quality_spinbox)
        spinbox_v_layout.addWidget(self.output_folder_lineedit)

        header_h_layout = HBoxLayout()
        header_h_layout.addLayout(label_v_layout)
        header_h_layout.addLayout(spinbox_v_layout)

        main_layout = VBoxLayout(self)
        main_layout.addLayout(header_h_layout)
        main_layout.addWidget(self.list_images)
        main_layout.addWidget(self.drop_label)
        main_layout.addWidget(self.compress_button)

        # Connections
        Shortcut(KeySequence("Delete"), self.list_images, self.delete_item)  # DEL
        self.compress_button.clicked.connect(self.convert_images)

    # Slots
    def delete_item(self):
        # get selected item
        items = self.list_images.selectedItems()
        if not items:
            return
        # delete
        for item in items:
            index = self.list_images.row(item)
            self.list_images.takeItem(index)

    def convert_images(self):
        size = self.size_spinbox.value() / 100.0
        quality = self.quality_spinbox.value()
        output_folder = self.output_folder_lineedit.text()
        if not output_folder:
            output_folder = 'Compressed_Images'

        nb_items = self.list_images.count()
        image_items = [self.list_images.item(index) for index in range(nb_items)
                       if not self.list_images.item(index).is_converted]

        if not image_items:
            warning_box = MessageBoxWarning("Warning", "No picture to convert")
            warning_box.exec()
            return

        #   conversion
        self.image_worker = Image_worker(image_items, output_folder, size, quality)
        self.image_worker.moveToThread(self.thread)
        # signals connect
        self.thread.started.connect(self.image_worker.convert)
        self.image_worker.converted.connect(self.converted_action)
        self.image_worker.finished.connect(self.thread.quit)

        self.thread.start()

        #   progress dialog
        self.progress_dialog = ProgressDialog("Progression...", "Cancel", 1, len(image_items))
        self.progress_dialog.canceled.connect(self.abort)
        self.progress_dialog.show()

    def abort(self):
        self.image_worker.run = False
        self.thread.quit()

    def converted_action(self, image_item, status):  # run when image.converted signal has emitted
        if status:
            image_item.setIcon(self.correct_icon)
            image_item.is_converted = True
            self.progress_dialog.setValue(self.progress_dialog.value() + 1)  # increment progress bar (+1)
        else:
            critical_box = MessageBoxCritical("Error", f"Can't compress {image_item.text()}")
            critical_box.exec()

    # Pre-builds slots (redefine to use), already connect to signal drop
    def dragEnterEvent(self, event):  # drop and enter app zone
        event.accept()
        self.drop_label.setVisible(True)

    def dragLeaveEvent(self, event):  # drop and quit app zone
        self.drop_label.setVisible(False)

    def dropEvent(self, event):  # drop and put
        event.accept()
        self.drop_label.setVisible(False)
        for url in event.mimeData().urls():
            self.add_pictures_to_list(url.toLocalFile())

    # Methods
    def add_pictures_to_list(self, image):
        # get all items
        nb_items = self.list_images.count()
        items_list = [self.list_images.item(index).text() for index in range(nb_items)]
        # verify if image not in list items
        if image not in items_list:
            new_item = ListWidgetItem(image)
            new_item.setIcon(self.warning_icon)
            new_item.is_converted = False  # Create new attribute for this ListWidgetItem
            self.list_images.addItem(new_item)
