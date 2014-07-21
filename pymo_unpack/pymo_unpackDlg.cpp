// pymo_unpackDlg.cpp : implementation file
//

#include "stdafx.h"
#include "pymo_unpack.h"
#include "pymo_unpackDlg.h"
#include  <vector> 
using   namespace   std; 

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif
#define BIF_USENEWUI 0x0050

/////////////////////////////////////////////////////////////////////////////
// CAboutDlg dialog used for App About

class CAboutDlg : public CDialog
{
public:
	CAboutDlg();

// Dialog Data
	//{{AFX_DATA(CAboutDlg)
	enum { IDD = IDD_ABOUTBOX };
	//}}AFX_DATA

	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CAboutDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:
	//{{AFX_MSG(CAboutDlg)
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialog(CAboutDlg::IDD)
{
	//{{AFX_DATA_INIT(CAboutDlg)
	//}}AFX_DATA_INIT
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CAboutDlg)
	//}}AFX_DATA_MAP
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialog)
	//{{AFX_MSG_MAP(CAboutDlg)
		// No message handlers
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CPymo_unpackDlg dialog

CPymo_unpackDlg::CPymo_unpackDlg(CWnd* pParent /*=NULL*/)
	: CDialog(CPymo_unpackDlg::IDD, pParent)
{
	//{{AFX_DATA_INIT(CPymo_unpackDlg)
	m_sRtDataFilePath = _T("");
	m_strExtension = _T("");
	m_strPath = _T("");
	//}}AFX_DATA_INIT
	// Note that LoadIcon does not require a subsequent DestroyIcon in Win32
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CPymo_unpackDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CPymo_unpackDlg)
	DDX_Text(pDX, IDC_EDIT1, m_sRtDataFilePath);
	DDX_Text(pDX, IDC_EDIT2, m_strExtension);
	DDX_Text(pDX, IDC_EDIT3, m_strPath);
	//}}AFX_DATA_MAP
}

BEGIN_MESSAGE_MAP(CPymo_unpackDlg, CDialog)
	//{{AFX_MSG_MAP(CPymo_unpackDlg)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_BN_CLICKED(IDC_BUTTON1, OnButton1)
	ON_BN_CLICKED(IDC_BUTTON3, OnButton3)
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CPymo_unpackDlg message handlers

BOOL CPymo_unpackDlg::OnInitDialog()
{
	CDialog::OnInitDialog();

	// Add "About..." menu item to system menu.

	// IDM_ABOUTBOX must be in the system command range.
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		CString strAboutMenu;
		strAboutMenu.LoadString(IDS_ABOUTBOX);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// Set the icon for this dialog.  The framework does this automatically
	//  when the application's main window is not a dialog
	SetIcon(m_hIcon, TRUE);			// Set big icon
	SetIcon(m_hIcon, FALSE);		// Set small icon
	
	// TODO: Add extra initialization here
	m_strExtension=".png";
	UpdateData(FALSE);
	return TRUE;  // return TRUE  unless you set the focus to a control
}

void CPymo_unpackDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialog::OnSysCommand(nID, lParam);
	}
}

// If you add a minimize button to your dialog, you will need the code below
//  to draw the icon.  For MFC applications using the document/view model,
//  this is automatically done for you by the framework.

void CPymo_unpackDlg::OnPaint() 
{
	if (IsIconic())
	{
		CPaintDC dc(this); // device context for painting

		SendMessage(WM_ICONERASEBKGND, (WPARAM) dc.GetSafeHdc(), 0);

		// Center icon in client rectangle
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// Draw the icon
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialog::OnPaint();
	}
}

// The system calls this to obtain the cursor to display while the user drags
//  the minimized window.
HCURSOR CPymo_unpackDlg::OnQueryDragIcon()
{
	return (HCURSOR) m_hIcon;
}

void CPymo_unpackDlg::OnButton1() 
{
	// TODO: Add your control notification handler code here
	UpdateData(TRUE);
	char szFilter[]="pymo pak files(*.pak)|*.pak";
	
	CFileDialog dlg(1,NULL,NULL,NULL,szFilter);
	
	if(dlg.DoModal()==IDOK)
	{
        m_sRtDataFilePath = dlg.GetPathName();
		if (GetFileAttributes(m_sRtDataFilePath) == -1){
			MessageBox("File does not exist!",NULL);
		}
		else
			UpdateData(FALSE);
	}
	
}

void CPymo_unpackDlg::OnButton3() 
{
	// TODO: Add your control notification handler code here
	UpdateData(TRUE);
	char szDir[MAX_PATH];
	BROWSEINFO bi;
	ITEMIDLIST *pidl;
	bi.hwndOwner = this->m_hWnd;
	bi.pidlRoot = NULL;
	bi.pszDisplayName = szDir;
	bi.lpszTitle = "Choose dir to save unpacked files";
	bi.ulFlags = BIF_STATUSTEXT | BIF_USENEWUI | BIF_RETURNONLYFSDIRS;
	bi.lpfn = NULL;
	bi.lParam = 0;
	bi.iImage = 0;
	pidl = SHBrowseForFolder(&bi);
	if(pidl == NULL)  return;
	if(!SHGetPathFromIDList(pidl, szDir))   return;
	else  m_strPath = szDir;
	UpdateData(FALSE);    
}

void CPymo_unpackDlg::OnOK() 
{
	// TODO: Add extra validation here
	UpdateData(TRUE);
	unsigned char filename[32];
	char *buf;
	unsigned int filelength,fileoffset,i,filecount;
    vector <int> offsetlist,lengthlist;
    vector <CString> filenamelist;
    CString filenamestring,strTmp;
	CFile file,pakfile;
	pakfile.Open(m_sRtDataFilePath, CFile::modeRead);
	pakfile.Read(&filecount, sizeof(unsigned int));
	for (i=0;i<filecount;i++){
	pakfile.Read(filename, 32);
	filenamestring=filename;
	filenamestring.MakeLower();
			filenamelist.push_back(filenamestring+m_strExtension);
	pakfile.Read(&fileoffset, sizeof(unsigned int));
	pakfile.Read(&filelength, sizeof(unsigned int));
			lengthlist.push_back(filelength);
			offsetlist.push_back(fileoffset);
	}
	for (i=0;i<filecount;i++){
		file.Open(m_strPath+"\\"+filenamelist[i], CFile::modeCreate|CFile::modeWrite);
		filelength=lengthlist[i];
		buf=new   char[filelength];
		pakfile.Seek(offsetlist[i],CFile::begin);
		pakfile.Read(buf,filelength); 
		file.Write(buf, filelength);
		delete   (buf);
		file.Close();
	}
	pakfile.Close();

	strTmp.Format( "%d files are unpacked.",filecount); 
	MessageBox(strTmp,NULL);
	//CDialog::OnOK();
}
