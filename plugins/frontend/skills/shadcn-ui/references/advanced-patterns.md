# Advanced Patterns

Detailed implementation patterns for shadcn/ui's most complex components.

## Data Table

3-file architecture integrating TanStack Table with shadcn's Table component.

### Column Definitions (columns.tsx)

```tsx
"use client"

import { ColumnDef } from "@tanstack/react-table"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
import { DataTableColumnHeader } from "./data-table-column-header"

export const columns: ColumnDef<Payment>[] = [
  // Row selection column
  {
    id: "select",
    header: ({ table }) => (
      <Checkbox
        checked={table.getIsAllPageRowsSelected() ||
          (table.getIsSomePageRowsSelected() && "indeterminate")}
        onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
        aria-label="Select all"
      />
    ),
    cell: ({ row }) => (
      <Checkbox
        checked={row.getIsSelected()}
        onCheckedChange={(value) => row.toggleSelected(!!value)}
        aria-label="Select row"
      />
    ),
    enableSorting: false,
    enableHiding: false,
  },
  // Sortable column with custom header
  {
    accessorKey: "status",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Status" />
    ),
    cell: ({ row }) => <Badge>{row.getValue("status")}</Badge>,
  },
  // Simple accessor column
  {
    accessorKey: "email",
    header: "Email",
  },
  // Formatted column
  {
    accessorKey: "amount",
    header: () => <div className="text-right">Amount</div>,
    cell: ({ row }) => {
      const formatted = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
      }).format(parseFloat(row.getValue("amount")))
      return <div className="text-right font-medium">{formatted}</div>
    },
  },
]
```

### Table Wrapper (data-table.tsx)

```tsx
"use client"

import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  SortingState,
  ColumnFiltersState,
  VisibilityState,
  RowSelectionState,
  flexRender,
} from "@tanstack/react-table"

export function DataTable<TData, TValue>({ columns, data }) {
  const [sorting, setSorting] = useState<SortingState>([])
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])
  const [columnVisibility, setColumnVisibility] = useState<VisibilityState>({})
  const [rowSelection, setRowSelection] = useState<RowSelectionState>({})

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onColumnVisibilityChange: setColumnVisibility,
    onRowSelectionChange: setRowSelection,
    state: { sorting, columnFilters, columnVisibility, rowSelection },
  })

  return (
    <div>
      {/* Toolbar: filter input + column visibility toggle */}
      <div className="flex items-center py-4">
        <Input
          placeholder="Filter emails..."
          value={(table.getColumn("email")?.getFilterValue() as string) ?? ""}
          onChange={(e) => table.getColumn("email")?.setFilterValue(e.target.value)}
          className="max-w-sm"
        />
        <DataTableViewOptions table={table} />
      </div>

      {/* Table */}
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <TableHead key={header.id}>
                    {header.isPlaceholder ? null :
                      flexRender(header.column.columnDef.header, header.getContext())}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow key={row.id} data-state={row.getIsSelected() && "selected"}>
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={columns.length} className="h-24 text-center">
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      {/* Pagination */}
      <DataTablePagination table={table} />
    </div>
  )
}
```

### Server Component Page (page.tsx)

```tsx
import { columns } from "./columns"
import { DataTable } from "./data-table"

async function getData(): Promise<Payment[]> {
  // Fetch from API or database
  return await db.payments.findMany()
}

export default async function PaymentsPage() {
  const data = await getData()
  return <DataTable columns={columns} data={data} />
}
```

### Advanced Data Table Components

- **DataTableColumnHeader** - dropdown with sort asc/desc/hide column
- **DataTablePagination** - page navigation + rows per page selector + selected row count
- **DataTableViewOptions** - column visibility toggle via DropdownMenuCheckboxItem
- **DataTableFacetedFilter** - multi-select filter with badges for active filters

---

## Form + Zod Validation

React Hook Form + Zod for type-safe, validated forms.

### Basic Form Setup

```tsx
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

const profileSchema = z.object({
  username: z.string().min(2, "Username must be at least 2 characters").max(30),
  email: z.string().email("Invalid email address"),
  bio: z.string().max(160).optional(),
  role: z.enum(["admin", "user", "editor"]),
  notifications: z.boolean().default(false),
})

type ProfileValues = z.infer<typeof profileSchema>

export function ProfileForm() {
  const form = useForm<ProfileValues>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      username: "",
      email: "",
      bio: "",
      role: "user",
      notifications: false,
    },
  })

  function onSubmit(values: ProfileValues) {
    // values is fully typed and validated
    console.log(values)
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
      {/* Input field */}
      <Field data-invalid={!!form.formState.errors.username}>
        <FieldLabel>Username</FieldLabel>
        <Input {...form.register("username")} aria-invalid={!!form.formState.errors.username} />
        <FieldDescription>Your public display name.</FieldDescription>
        <FieldError>{form.formState.errors.username?.message}</FieldError>
      </Field>

      {/* Select field */}
      <Controller
        control={form.control}
        name="role"
        render={({ field }) => (
          <Field>
            <FieldLabel>Role</FieldLabel>
            <Select value={field.value} onValueChange={field.onChange}>
              <SelectTrigger><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="admin">Admin</SelectItem>
                <SelectItem value="user">User</SelectItem>
                <SelectItem value="editor">Editor</SelectItem>
              </SelectContent>
            </Select>
            <FieldError>{form.formState.errors.role?.message}</FieldError>
          </Field>
        )}
      />

      {/* Switch field */}
      <Controller
        control={form.control}
        name="notifications"
        render={({ field }) => (
          <Field>
            <div className="flex items-center gap-2">
              <Switch checked={field.value} onCheckedChange={field.onChange} />
              <FieldLabel>Enable notifications</FieldLabel>
            </div>
          </Field>
        )}
      />

      <Button type="submit">Save</Button>
    </form>
  )
}
```

### Dynamic Field Arrays

```tsx
const { fields, append, remove } = useFieldArray({
  control: form.control,
  name: "urls",
})

return (
  <div>
    {fields.map((field, index) => (
      // CRITICAL: use field.id as key, NOT index
      <div key={field.id} className="flex gap-2">
        <Input {...form.register(`urls.${index}.value`)} />
        <Button variant="outline" onClick={() => remove(index)}>Remove</Button>
      </div>
    ))}
    <Button variant="outline" onClick={() => append({ value: "" })}>Add URL</Button>
  </div>
)
```

### Validation Modes

| Mode | Behavior |
|------|----------|
| `onSubmit` (default) | Validate on form submission |
| `onChange` | Validate on every change (expensive) |
| `onBlur` | Validate when field loses focus |
| `onTouched` | Validate on first blur, then on every change |
| `all` | Validate on both blur and change |

---

## Sidebar Navigation

Provider-based architecture for responsive, collapsible navigation.

### Full Layout Setup

```tsx
import {
  SidebarProvider,
  Sidebar,
  SidebarHeader,
  SidebarContent,
  SidebarFooter,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarMenuSub,
  SidebarMenuSubItem,
  SidebarMenuAction,
  SidebarMenuBadge,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarTrigger,
} from "@/components/ui/sidebar"

export default function AppLayout({ children }) {
  return (
    <SidebarProvider>
      <Sidebar collapsible="icon">
        <SidebarHeader>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton asChild>
                <a href="/"><Logo /> App Name</a>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarHeader>

        <SidebarContent>
          {/* Collapsible group */}
          <Collapsible defaultOpen>
            <SidebarGroup>
              <SidebarGroupLabel asChild>
                <CollapsibleTrigger>
                  Platform
                  <ChevronDown className="ml-auto transition-transform group-data-[state=open]/collapsible:rotate-180" />
                </CollapsibleTrigger>
              </SidebarGroupLabel>
              <CollapsibleContent>
                <SidebarMenu>
                  <SidebarMenuItem>
                    <SidebarMenuButton asChild>
                      <a href="/dashboard"><LayoutDashboard /> Dashboard</a>
                    </SidebarMenuButton>
                    <SidebarMenuBadge>12</SidebarMenuBadge>
                  </SidebarMenuItem>

                  {/* Nested submenu */}
                  <SidebarMenuItem>
                    <SidebarMenuButton>
                      <Settings /> Settings
                    </SidebarMenuButton>
                    <SidebarMenuSub>
                      <SidebarMenuSubItem>
                        <SidebarMenuButton asChild>
                          <a href="/settings/profile">Profile</a>
                        </SidebarMenuButton>
                      </SidebarMenuSubItem>
                      <SidebarMenuSubItem>
                        <SidebarMenuButton asChild>
                          <a href="/settings/security">Security</a>
                        </SidebarMenuButton>
                      </SidebarMenuSubItem>
                    </SidebarMenuSub>
                  </SidebarMenuItem>
                </SidebarMenu>
              </CollapsibleContent>
            </SidebarGroup>
          </Collapsible>
        </SidebarContent>

        <SidebarFooter>
          {/* User menu, etc. */}
        </SidebarFooter>
      </Sidebar>

      <main className="flex-1">
        <header className="flex items-center gap-2 p-4 border-b">
          <SidebarTrigger />
          <h1>Page Title</h1>
        </header>
        {children}
      </main>
    </SidebarProvider>
  )
}
```

### Collapsible Modes

| Mode | Behavior |
|------|----------|
| `collapsible="icon"` | Collapses to icon-only rail |
| `collapsible="offcanvas"` | Slides in/out from edge (mobile) |
| `collapsible="none"` | Always visible, not collapsible |

### useSidebar() Hook

```tsx
const {
  state,          // "expanded" | "collapsed"
  open,           // boolean (desktop)
  setOpen,        // (open: boolean) => void
  openMobile,     // boolean (mobile)
  setOpenMobile,  // (open: boolean) => void
  isMobile,       // boolean
  toggleSidebar,  // () => void
} = useSidebar()
```

### CSS Variables

```css
:root {
  --sidebar-width: 16rem;
  --sidebar-width-mobile: 18rem;
  --sidebar-width-icon: 3rem;
}
```

---

## Dialog Patterns

### Scrollable Dialog with Sticky Footer

```tsx
<Dialog>
  <DialogContent className="max-h-[80vh] flex flex-col">
    <DialogHeader>
      <DialogTitle>Long Content</DialogTitle>
    </DialogHeader>
    <div className="flex-1 overflow-y-auto py-4">
      {/* scrollable content */}
    </div>
    <div className="flex justify-end gap-2 border-t pt-4">
      <Button variant="outline">Cancel</Button>
      <Button>Confirm</Button>
    </div>
  </DialogContent>
</Dialog>
```

### Headless Dialog (Custom Close)

```tsx
<DialogContent showCloseButton={false}>
  {/* You control the close mechanism */}
  <DialogClose asChild>
    <Button>Done</Button>
  </DialogClose>
</DialogContent>
```
