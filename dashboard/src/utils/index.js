export function isImage(extention) {
	if (!extention) return false;
	return ["png", "jpg", "jpeg", "gif", "svg", "bmp", "webp"].includes(extention.toLowerCase());
}

export function validateIsImageFile(file) {
	const extn = file.name.split(".").pop().toLowerCase();
	if (!isImage(extn)) {
		return "Only image files are allowed";
	}
}
