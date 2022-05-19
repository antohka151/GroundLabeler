from IO import *
from processing import *
from colorama import init, Fore

EXIT_LIST = ['quit', 'q', 'exit', 'e']
UPDATE_LIST = ['update', 'u']
DONE_LIST = ['done', 'd', 'labelled']
HELP_LIST = ['help', 'h']
AUTO_LIST = ['auto', 'a']
SHORTCUTS = {'odd': [i for i in range(11, 32, 2)], 'even': [i for i in range(12, 33, 2)],
             'lfoot': [29, 31], 'rfoot': [30, 32], 'lhand': [15, 17, 19], 'rhand': [16, 18, 20]}


def _label_video_help():
    print()
    print(Fore.GREEN + "Shortcut list:")
    print(Fore.GREEN + "  'odd' - all odd key points (left part of the body)")
    print(Fore.GREEN + "  'even' - all even key points (right part of the body)")
    print(Fore.GREEN + "  'lfoor' or 'rfoot' - left or right foot (stopa)")
    print(Fore.GREEN + "  'lhand' or 'rhand' - left or right hand (licevaya chast)")
    print()


def _label_video_end(video_name, was_something_done):
    print()
    print(Fore.LIGHTGREEN_EX + "Thank you for labelling video")
    print(Fore.LIGHTGREEN_EX + "Was video fully labelled? [y/n]")
    answer = input().lower()
    if answer == 'y' or answer == 'yes':
        update_video_list(video_name, labelled=True, skipped=False, force=True)
    elif was_something_done:
        update_video_list(video_name, labelled=True, skipped=True)
    else:
        update_video_list(video_name, skipped=True)
    annotated_vp = os.path.join('assets', 'labelling_video', 'annotated_' + video_name.split('.')[0] + '.mp4')
    if os.path.exists(annotated_vp):
        os.remove(annotated_vp)
    print()


def label_video(vid_name):
    print()
    print(Fore.LIGHTRED_EX + "Print 'help' or 'h' to get shortcut list")
    print(Fore.LIGHTRED_EX + "'exit' or 'e' to end labelling process, 'update' or 'u' to update video")
    was_something_done = False
    max_frame = pd.read_csv(os.path.join('assets', 'videos_csv', vid_name.split('.')[0] + '.csv')).iloc[-1]['frame']
    while True:
        print('-' * 40)
        print(Fore.LIGHTCYAN_EX + "Please enter key points or shortcuts:")
        print(Fore.LIGHTCYAN_EX + "f.e. [6 odd 18]")

        print()
        kpoints = input()
        try:
            if kpoints in UPDATE_LIST:
                process_videos(vid_name)
                continue
            elif kpoints in HELP_LIST:
                _label_video_help()
                continue
            elif kpoints in EXIT_LIST or kpoints in DONE_LIST:
                _label_video_end(vid_name, was_something_done)
                return
            numbers = []
            for kpoint in kpoints.split():
                if kpoint in SHORTCUTS.keys():
                    numbers += SHORTCUTS[kpoint]
                elif 0 <= int(kpoint) < 33:
                    numbers.append(int(kpoint))
                else:
                    print(Fore.RED + "Couldn't recognize your key point number or shortcut")
                    print(Fore.RED + "Are you sure this key points exist?")
                    raise ValueError
            numbers = set(numbers)
            print()
            print(Fore.LIGHTBLUE_EX + "Please enter frame range: frame1 frame2")
            print(Fore.LIGHTBLUE_EX + "f.e. 15 25 (is equal to 15<=X<=25 )")
            print()
            frame_range = list(map(int, input().split()))
            if min(frame_range) < 1 or max(frame_range) > max_frame or not (1 <= len(frame_range) <= 2):
                print(Fore.RED + "Frame range error")
                raise ValueError
            else:
                if len(frame_range) == 2:
                    f1, f2 = frame_range
                else:
                    f1 = f2 = frame_range[0]
            print()
            print(Fore.BLUE + "Enter flag value (1 - On the floor, 0 - in air)")
            print()
            fvalue = int(input())
            if not (0 <= fvalue <= 1):
                print(Fore.RED + "Flag value error")
                raise ValueError
        except ValueError:
            print()
            print(Fore.LIGHTRED_EX + "Wrong input. Please try again.")
            print(Fore.LIGHTRED_EX + "Print 'help' or 'h' to get shortcut list")
            print(Fore.LIGHTRED_EX + "'exit' or 'e' to end labelling process, 'update' or 'u' to update video")
            print()
            continue
        df = pd.read_csv(os.path.join("assets", "videos_csv", vid_name.split('.')[0] + ".csv"))
        for frame in range(f1, f2+1):
            for num in numbers:
                df.loc[(frame-1)*33 + num, 'flag'] = fvalue
        df.to_csv(os.path.join("assets", "videos_csv", vid_name.split('.')[0] + ".csv"), index=False)
        was_something_done = True


def labelling_start():
    print()
    print(Fore.LIGHTGREEN_EX + "Hello, please choose video to label")
    print(Fore.LIGHTGREEN_EX + "Print 'auto' or 'a' for video to automatically be chosen")
    print(Fore.LIGHTGREEN_EX + "Or just type the video name")
    print()
    mode = input()
    if mode.lower() in EXIT_LIST:
        print(Fore.LIGHTRED_EX + "Exiting labelling process")
        exit(0)
    elif mode.lower() in AUTO_LIST:
        vid_name = get_video_auto()
        # If vid_name == 1: all videos were labelled
        if vid_name != -1:
            process_videos(vid_name)
            label_video(vid_name)
    else:
        print(Fore.LIGHTYELLOW_EX + f"Your video name is {mode}? [y/n]")
        print(Fore.LIGHTYELLOW_EX + "Example of right video name - vidname.mp4")
        print()
        answer = input().lower()
        if answer in ("y", "yes"):
            process_videos(mode)
            label_video(mode)
        else:
            print(Fore.LIGHTRED_EX + "Please try again")
            return


def main():
    #clear_videos_list()
    while True:
        update_video_list(load_videos_folder(os.path.join('assets', 'videos')))
        labelling_start()


if __name__ == '__main__':
    init(autoreset=True)
    main()
