import re

# Farb-Codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


def format_timecode(input_str):
    digits = re.sub(r'\D', '', input_str)
    if len(digits) != 6:
        return None
    hh, mm, ss = int(digits[:2]), int(digits[2:4]), int(digits[4:6])
    if mm > 59 or ss > 59:
        return None
    return f"{hh:02}:{mm:02}:{ss:02}.000"


def input_loop(prompt, allow_empty=False):
    while True:
        value = input(prompt).strip()
        if value.lower() == 'q':
            print(f"{YELLOW}Beendet durch 'q'{RESET}")
            return 'q'
        elif value.lower() == 'x':
            return 'x'
        elif not value and not allow_empty:
            continue
        return value


def main():
    chapters = []
    step_stack = ['chapters']  # Speicher für "Zurück"-Navigation
    chapter_counter = 1

    print(f"""{YELLOW}
    ┌───────────────────────────────────────────┐
    │ 's' = Speichern | 'x' = Zurück / Löschen  │
    │ 'l' = Liste     | 'q' = Beenden 'STRG + C'│
    └───────────────────────────────────────────┘
    {RESET}""")

    format_choice = None
    filename_input = None
    lang_input = None
    full_length_formatted = None

    try:
        while True:
            current_step = step_stack[-1]

            if current_step == 'chapters':
                user_input = input(f"Zeitstempel {chapter_counter} eingeben: ").strip().lower()

                if user_input == 'q':
                    print(f"{YELLOW}Beendet durch Benutzereingabe 'q'{RESET}")
                    return
                if user_input == 's':
                    if not chapters:
                        print(f"{YELLOW}ℹ️  Keine Kapitel vorhanden!{RESET}")
                        continue
                    step_stack.append('choose_format')
                    continue
                if user_input == 'x':
                    if chapters:
                        last_time, last_name = chapters.pop()
                        chapter_counter -= 1
                        print(f"{YELLOW}⏪ Kapitel {chapter_counter} gelöscht: [{last_time} | {last_name}]{RESET}")
                    else:
                        print(f"{YELLOW}ℹ️  Keine Kapitel zum Zurückgehen vorhanden!{RESET}")
                    continue
                if user_input == 'l':
                    if not chapters:
                        print(f"{YELLOW}ℹ️  Keine Kapitel vorhanden!{RESET}")
                    else:
                        print(f"{GREEN}🔖 Kapitelübersicht:{RESET}")
                        for idx, (timecode, name) in enumerate(chapters, start=1):
                            print(f"{CYAN}CHAPTER{idx:02}={timecode}{RESET}")
                            print(f"{CYAN}CHAPTER{idx:02}NAME={name}{RESET}")
                    continue

                formatted = format_timecode(user_input)
                if not formatted:
                    print(f"{RED}⚠️  Ungültiger Zeitstempel: {user_input}{RESET}")
                    continue

                while True:
                    name_input = input(f"Kapitel Name {chapter_counter} eingeben: ").strip()
                    if name_input.lower() == 'q':
                        print(f"{YELLOW}Beendet durch 'q'{RESET}")
                        return
                    if name_input.lower() == 's':
                        print(f"{YELLOW}ℹ️  Du brauchst einen Kapitelname um Speicher zu können!{RESET}")
                        continue
                    if name_input.lower() == 'x':
                        print(f"{YELLOW}⏪ Zurück zu Zeitstempel {chapter_counter}...{RESET}")
                        break
                    if name_input.lower() == 'l':
                        if not chapters:
                            print(f"{YELLOW}ℹ️  Keine Kapitel zum Anzeigen vorhanden!{RESET}")
                        else:
                            print(f"{GREEN}🔖 Kapitelübersicht:{RESET}")
                            for idx, (timecode, name) in enumerate(chapters, start=1):
                                print(f"{CYAN}CHAPTER{idx:02}={timecode}{RESET}")
                                print(f"{CYAN}CHAPTER{idx:02}NAME={name}{RESET}")
                        continue
                    if not name_input:
                        name_input = f"Chapter {chapter_counter:02}"

                    chapters.append((formatted, name_input))
                    chapter_counter += 1
                    break

            elif current_step == 'choose_format':
                user_input = input("Welches Format? TXT | XML | 'b' Beide: ").strip().lower()
                if user_input == 'q':
                    print(f"{YELLOW}Beendet durch 'q'{RESET}")
                    return
                if user_input == 'x':
                    step_stack.pop()
                    continue
                if user_input in ['txt', 'xml', 'b']:
                    format_choice = user_input
                    step_stack.append('choose_filename')
                else:
                    print(f"{RED}⚠️ Ungültige Eingabe: {user_input}{RESET}")

            elif current_step == 'choose_filename':
                filename_input = input_loop("Dateiname für die Kapitelliste: ", allow_empty=True)
                if filename_input == 'q':
                    return
                if filename_input == 'x':
                    step_stack.pop()
                    continue
                if not filename_input:
                    filename_input = "Kapitel"
                if format_choice in ['xml', 'b']:
                    step_stack.append('xml_lang')
                else:
                    step_stack.append('save')

            elif current_step == 'xml_lang':
                while True:
                    lang_input = input_loop("XML-Sprache (zB. eng, deu): ", allow_empty=True)
                    if lang_input == 'q':
                        return
                    if lang_input == 'x':
                        step_stack.pop()
                        break
                    if not lang_input:
                        lang_input = "eng"
                    if not (lang_input.isalpha() and len(lang_input) == 3):
                        print(f"{RED}⚠️ Ungültiger Sprache! {lang_input}{RESET}")
                        continue
                    step_stack.append('xml_length')
                    break

            elif current_step == 'xml_length':
                full_length = input_loop("Volle Videolänge (zB. 01:23:45): ", allow_empty=True)
                if full_length == 'q':
                    return
                if full_length == 'x':
                    step_stack.pop()
                    continue
                full_length_formatted = format_timecode(full_length)
                if not full_length_formatted:
                    print(f"{RED}⚠️ Ungültiger Videolänge: {full_length}{RESET}")
                    continue
                step_stack.append('save')

            elif current_step == 'save':
                # TXT speichern
                if format_choice in ['txt', 'b']:
                    path_txt = f"{filename_input}_chapters.txt"
                    with open(path_txt, "w", encoding="utf-8") as f:
                        for idx, (tc, name) in enumerate(chapters, start=1):
                            f.write(f"CHAPTER{idx:02}={tc}\n")
                            f.write(f"CHAPTER{idx:02}NAME={name}\n")
                    print(f"{GREEN}TXT gespeichert: {path_txt}{RESET}")

                # XML speichern
                if format_choice in ['xml', 'b']:
                    path_xml = f"{filename_input}_chapters.xml"
                    with open(path_xml, "w", encoding="utf-8") as f:
                        f.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
                        f.write('<!DOCTYPE Chapters SYSTEM "matroskachapters.dtd">\n')
                        f.write('<Chapters>\n  <EditionEntry>\n')
                        for i in range(len(chapters)):
                            start = chapters[i][0]
                            end = chapters[i + 1][0] if i + 1 < len(chapters) else full_length_formatted
                            name = chapters[i][1]
                            f.write("    <ChapterAtom>\n")
                            f.write(f"      <ChapterTimeStart>{start}</ChapterTimeStart>\n")
                            f.write(f"      <ChapterTimeEnd>{end}</ChapterTimeEnd>\n")
                            f.write("      <ChapterDisplay>\n")
                            f.write(f"        <ChapterString>{name}</ChapterString>\n")
                            f.write(f"        <ChapterLanguage>{lang_input}</ChapterLanguage>\n")
                            f.write("      </ChapterDisplay>\n")
                            f.write("    </ChapterAtom>\n")
                        f.write("  </EditionEntry>\n</Chapters>\n")
                    print(f"{GREEN}XML gespeichert: {path_xml}{RESET}")
                return

    except KeyboardInterrupt:
        print(f"\n{YELLOW}Beendet durch STRG+C{RESET}")


if __name__ == "__main__":
    main()
