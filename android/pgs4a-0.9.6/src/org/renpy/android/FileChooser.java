package org.renpy.android;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileFilter;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.Arrays;
import java.util.Comparator;
import java.util.ArrayList;
import java.util.HashMap;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ComponentName;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.Intent.ShortcutIconResource;
import android.os.Bundle;
import android.content.Context;
import android.graphics.Color;
import android.graphics.Rect;
import android.view.View;
import android.view.WindowManager;
import android.view.Display;
import android.view.Gravity;
import android.os.Environment;
import android.widget.TextView;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.AdapterView;
import android.widget.Toast;
import android.util.Log;
import android.net.Uri;

public class FileChooser extends Activity implements AdapterView.OnItemClickListener, Runnable {
	private File mCurrentDirectory = null;
	private File mOldCurrentDirectory = null;
	private File[] mDirectoryFiles = null;
	private ListView listView = null;
	private int set_executed_time=0;
	private int set_original_ratio = 0;
	private int set_keypad_extend = 0;
	private int set_keypad_horizontal = 1;
	private String set_last_path;
	private String line_read;
	private SimpleAdapter listItemAdapter;
	private ArrayList<HashMap<String, Object>> listItems;
	private HashMap<String, Object> map;

    private ResourceManager resourceManager;

	static class FileSort implements Comparator<File> {
		public int compare(File src, File target) {
			return src.getName().compareTo(target.getName());
		}
	}

	private void setupDirectorySelector() {
		mDirectoryFiles = mCurrentDirectory.listFiles(new FileFilter() {
			public boolean accept(File file) {
				return (!file.isHidden() && file.isDirectory());
			}
		});

		Arrays.sort(mDirectoryFiles, new FileSort());

		String names;

		listItems = new ArrayList<HashMap<String, Object>>();

		if (mCurrentDirectory.getParent() != null) {
			names = "..";
			map = new HashMap<String, Object>();
			map.put("ItemTitle", "..");
			listItems.add(map);
		}
		for (int i = 0; i < mDirectoryFiles.length; i++) {
			names = mDirectoryFiles[i].getName();

			String gameconfigPath = mDirectoryFiles[i].toString() + "/gameconfig.txt";
			String iconPath = mDirectoryFiles[i].toString() + "/icon.png";
			File gameconfig = new File(gameconfigPath);

			if (mDirectoryFiles[i].isDirectory() && gameconfig.exists()) {
				try {
					BufferedReader br = new BufferedReader(new FileReader(gameconfig));
					line_read=br.readLine();
					while (line_read != null){
						
						String[] sArray=line_read.split(",");
						if (sArray[0].equals("gametitle")){
							names=sArray[1].replace("\\n", "\n");
						}
						line_read=br.readLine();
					} 
					br.close();
					
				} catch (FileNotFoundException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}

			map = new HashMap<String, Object>();

			map.put("ItemTitle", names); // 閺傚洤鐡�
			map.put("ItemImage", iconPath); // 閸ュ墽澧�
			listItems.add(map);
		}
		View current_view=resourceManager.inflateView("list_item");
		listItemAdapter = new SimpleAdapter(this, listItems, // listItems閺佺増宓侀敓锟�
				resourceManager.getIdentifier("list_item", "layout"), // ListItem閻ㄥ垕ML鐢啫鐪�鐐靛箛
				new String[] { "ItemTitle", "ItemImage" }, // 閸斻劍锟介弫鎵矋娑撳丢mageItem鐎电懓绨查惃鍕摍閿燂拷
				new int[] { resourceManager.getIdentifier("ItemTitle", "id"), resourceManager.getIdentifier("ItemImage", "id") });
		// ArrayAdapter<String> arrayAdapter = new ArrayAdapter<String>(this,
		// android.R.layout.simple_list_item_1, names);
		
		listView.setAdapter(listItemAdapter);
		listView.setOnItemClickListener(this);
	}

	private void runLauncher() {
		mCurrentDirectory = new File(gCurrentDirectoryPath);
		if (mCurrentDirectory.exists() == false) {
			if (!android.os.Environment.getExternalStorageState().equals(
					android.os.Environment.MEDIA_MOUNTED)) {
				gCurrentDirectoryPath = Environment.getRootDirectory()
						.getPath();
				mCurrentDirectory = new File(gCurrentDirectoryPath);
			} else {
				gCurrentDirectoryPath = Environment
						.getExternalStorageDirectory().getPath();
				mCurrentDirectory = new File(gCurrentDirectoryPath);
			}

			if (mCurrentDirectory.exists() == false)
				Toast.makeText(this, "Could not find SD card.",
						Toast.LENGTH_SHORT).show();
				finish();
		}

		listView = new ListView(this);
		listView.setBackgroundColor(0x30303080);
		listView.setCacheColorHint(0x05050505);
		listView.setPersistentDrawingCache(ListView.PERSISTENT_ALL_CACHES);
		listView.setScrollingCacheEnabled(true);
		listView.setAlwaysDrawnWithCacheEnabled(true);

		currentPath = new TextView(this);
		currentPath.setText(gCurrentDirectoryPath);
		currentPath.setTextSize(20);
		currentPath.setGravity(Gravity.CENTER_VERTICAL);
		currentPath.setBackgroundDrawable(getResources().getDrawable(
                android.R.drawable.title_bar));
		currentPath.setTextColor(Color.WHITE);
		listView.addHeaderView(currentPath, null, false);

		setupDirectorySelector();

		setContentView(listView);
	}

	public void onItemClick(AdapterView<?> parent, View v, int position, long id) {
		position--; // for header

		TextView textView = (TextView) resourceManager.getViewById(v,"ItemTitle");
		mOldCurrentDirectory = mCurrentDirectory;

		if (textView.getText().equals("..")) {
			mCurrentDirectory = new File(mCurrentDirectory.getParent());
			gCurrentDirectoryPath = mCurrentDirectory.getPath();
		} else {
			if (mCurrentDirectory.getParent() != null)
				position--;
			gCurrentDirectoryPath = mDirectoryFiles[position].getPath();
			mCurrentDirectory = new File(gCurrentDirectoryPath);
		}

		mDirectoryFiles = mCurrentDirectory.listFiles(new FileFilter() {
			public boolean accept(File file) {
				return (file.isFile() && (file.getName().equals("gameconfig.txt")));
			}
		});
		
		if (mDirectoryFiles==null){
			mCurrentDirectory = mOldCurrentDirectory;
			gCurrentDirectoryPath=mCurrentDirectory.getPath();
			setupDirectorySelector();
		}
		else if (mDirectoryFiles.length == 0) {
			setupDirectorySelector();
		} else {
			gCurrentDirectoryPath=mCurrentDirectory.getPath();
			set_last_path=gCurrentDirectoryPath;

			String gameconfigPath = gCurrentDirectoryPath + "/gameconfig.txt";
			File gameconfig = new File(gameconfigPath);
			String extension=".jpg";
			if (gameconfig.exists()) {
				try {
					BufferedReader br = new BufferedReader(new FileReader(gameconfig));
					line_read=br.readLine();
					while (line_read != null){
						
						String[] sArray=line_read.split(",");
						if (sArray[0].equals("bgformat")){
							extension=sArray[1];
						}
						line_read=br.readLine();
					} 
					br.close();
					
				} catch (FileNotFoundException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
			Log.v("Filechooser", extension);
			unpack_file(gCurrentDirectoryPath+"/bg/bg.pak","logo1",extension);
			
			Intent intent = new Intent();
			intent.setClassName(getPackageName(), "org.renpy.android.PythonActivity");
			this.startActivity(intent);
			this.finish();
		}
		currentPath.setText(gCurrentDirectoryPath);
	}

	public void unpack_file(String pak_path,String file_path,String file_extension){
		File pak_file=new File(pak_path);	
		File unpacked_file=new File(pak_file.getParent()+"/"+file_path+file_extension);
		File dest_file= new File(getFilesDir()+"/presplash.jpg");
		try {
			if (unpacked_file.exists()){
				FileInputStream inStream = new FileInputStream(unpacked_file);
				FileOutputStream outStream = new FileOutputStream(dest_file);
				byte[] buffer = new byte[1024];
				int length;
				//copy the file content in bytes 
				while ((length = inStream.read(buffer)) > 0){
					outStream.write(buffer, 0, length);
				}
				inStream.close();
				outStream.close();
			}
			else{
				RandomAccessFile inStream = new RandomAccessFile(pak_path,"r");
				int total_file_num = swapEndian(inStream.readInt());
				int i=0,j,file_offset,file_length;
				byte[] buffer = new byte[32];
				while (i<total_file_num){
					inStream.read(buffer, 0, 32);
					file_offset=swapEndian(inStream.readInt());
					file_length=swapEndian(inStream.readInt());
					for (j = 0; j < buffer.length && buffer[j] != 0; j++) { }
					String file_name = new String(buffer, 0, j);
					if (file_name.equals(file_path.toUpperCase())){
						
						byte[] buffer2 = new byte[file_length];
						inStream.seek(file_offset);
						if ( inStream.read(buffer2)==file_length ){
							FileOutputStream outStream = new FileOutputStream(dest_file);
							outStream.write(buffer2, 0, file_length);
							outStream.close();
						}
						break;
					}
					i+=1;
				}
				inStream.close();
		    	Log.v("FileChooser", "dest_file="+dest_file.getPath());
			}
		} catch (Exception e) {
			Log.v("FileChooser", "unpack file failed");
		}
	}
	private int swapEndian(int i){
	    return((i&0xff)<<24)+((i&0xff00)<<8)+((i&0xff0000)>>8)+((i>>24)&0xff);
	}
	public void WriteSetting(String globalconfigpath) {
		FileWriter fw;
		try {
			fw = new FileWriter(globalconfigpath);
			fw.write("last_path,"+set_last_path+"\r\n");
			fw.write("executed_time,"+set_executed_time+"\r\n");
			fw.write("original_ratio,"+set_original_ratio+"\r\n");
			fw.write("keypad_extend,"+set_keypad_extend+"\r\n");
			fw.write("keypad_horizontal,"+set_keypad_horizontal+"\r\n");
			fw.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public void ReadSetting(String globalconfigpath) {
		File globalconfig = new File(globalconfigpath);
		if (globalconfig.exists()) {
			try {
				BufferedReader br = new BufferedReader(new FileReader(globalconfig));
				line_read=br.readLine();
				while (line_read != null){
					String[] sArray=line_read.split(",");
					if (sArray[0].equals("last_path")) set_last_path =sArray[1];
					else if (sArray[0].equals("executed_time")) set_executed_time = Integer.parseInt(sArray[1]);
					else if (sArray[0].equals("original_ratio")) set_original_ratio=Integer.parseInt(sArray[1]);
					else if (sArray[0].equals("keypad_extend")) set_keypad_extend=Integer.parseInt(sArray[1]);
					else if (sArray[0].equals("keypad_horizontal")) set_keypad_horizontal=Integer.parseInt(sArray[1]);
					line_read=br.readLine();
				} 
				br.close();
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}

	public void About() {
		AlertDialog.Builder builder = new AlertDialog.Builder(this);
		builder.setTitle(resourceManager.getString("info_title"));
		builder.setMessage(resourceManager.getString("info"));
		builder.setPositiveButton("确定", null);
		builder.setNegativeButton("访问官网",
				new DialogInterface.OnClickListener() {
					public void onClick(DialogInterface dialog, int whichButton) {
						Uri uri = Uri.parse("http://pymo.github.io");
						Intent web = new Intent(Intent.ACTION_VIEW, uri);
						startActivity(web);
					}
				});

		builder.create().show();
	}

	@Override
	public void run() {
	}


	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
        resourceManager = new ResourceManager(this);
		gCurrentDirectoryPath = Environment.getExternalStorageDirectory().getPath();
		set_last_path=gCurrentDirectoryPath;
		ReadSetting(getFilesDir()+"/globalconfig.txt");
		if (!gCurrentDirectoryPath.equals(set_last_path)){
			mCurrentDirectory = new File(set_last_path);
			gCurrentDirectoryPath=mCurrentDirectory.getParent();
		}
		runLauncher();
		if (set_executed_time == 0) {
			About();
		}
		set_executed_time++;

	}
    @Override
    protected void onPause() {
        super.onPause();
        WriteSetting(getFilesDir()+"/globalconfig.txt");
    }
    @Override
    protected void onResume() {
        super.onResume();
        ReadSetting(getFilesDir()+"/globalconfig.txt");
    }
    
	public static String gCurrentDirectoryPath;
	public static TextView currentPath;


}