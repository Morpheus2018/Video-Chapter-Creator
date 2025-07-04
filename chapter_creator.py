import re
import sys

def format_timecode(input_str):
    digits = re.sub(r'\D', '', input_str)

    if len(digits) != 6:
        return None

    hh = int(digits[0:2])
    mm = int(digits[2:4])
    ss = int(digits[4:6])

    if mm > 59 or ss > 59:
        return None

    return f"{hh:02}:{mm:02}:{ss:02}.000"

def main():
    filepath = None  # Wichtig: vordefinieren für den Fall von Strg+C

    try:
        filename_input = input("Dateiname zum Kapitel erstellen eingeben: ").strip()
        if filename_input.lower() == 'q':
            print("Beendet durch Benutzereingabe.")
            sys.exit(0)
        if not filename_input:
            filename_input = "Kapitel"

        filepath = f"{filename_input}_chapters.txt"

        with open(filepath, "w", encoding="utf-8"):
            pass

        print("\n(Hinweis: Zum Beenden 'q' eingeben oder Strg+C drücken)")
        print(f"(Datei {filepath} wurde erfolgreich erstellt !!!)\n")

        chapter_counter = 1

        while True:
            user_input = input(f"Zeitstempel {chapter_counter} eingeben: ")
            if user_input.lower() == 'q':
                print("Beendet durch Benutzereingabe.")
                break

            formatted = format_timecode(user_input)

            if formatted:
                chapter_str = f"CHAPTER{chapter_counter:02}"
                print(f"{chapter_str}={formatted}")

                name_input = input(f"Kapitel Name {chapter_counter} eingeben: ").strip()
                if name_input.lower() == 'q':
                    print("Beendet durch Benutzereingabe q.")
                    break

                if not name_input:
                    name_input = f"Chapter {chapter_counter:02}"

                print(f"{chapter_str}NAME={name_input}")

                with open(filepath, "a", encoding="utf-8") as f:
                    f.write(f"{chapter_str}={formatted}\n")
                    f.write(f"{chapter_str}NAME={name_input}\n")

                chapter_counter += 1
            else:
                print(f"Dein Zeitstempel: {user_input} war Falsch. Versuch nochmal !!")

    except KeyboardInterrupt:
        print("\n\nProgramm durch Strg+C abgebrochen.")

    # Nur anzeigen, wenn filepath gesetzt wurde (Datei existiert)
    if filepath:
        print(f"\nAlle zuvor erstellten Kapitel sind gespeichert in: {filepath}")

if __name__ == "__main__":
    main()